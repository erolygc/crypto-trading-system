"""
Position Sizing Module
Portfolio yönetimi ve risk kontrolü için pozisyon boyutlandırma algoritmaları
"""

import numpy as np
import pandas as pd
from typing import Dict, Optional, Tuple
from dataclasses import dataclass
import logging

logger = logging.getLogger(__name__)

@dataclass
class RiskConfig:
    """Risk yönetimi konfigürasyonu"""
    max_portfolio_risk: float = 0.02  # %2 maksimum portföy riski
    max_position_risk: float = 0.01   # %1 maksimum pozisyon riski
    max_positions: int = 10           # Maksimum açık pozisyon sayısı
    min_trade_size: float = 10.0      # Minimum işlem büyüklüğü (USDT)
    max_trade_size: float = 1000.0    # Maksimum işlem büyüklüğü (USDT)

class PositionSizer:
    """
    Pozisyon boyutlandırma algoritmaları
    """
    
    def __init__(self, risk_config: RiskConfig = None):
        self.risk_config = risk_config or RiskConfig()
        self.position_history = []
        
    def kelly_criterion(self, win_rate: float, avg_win: float, avg_loss: float) -> float:
        """
        Kelly Criterion ile optimal pozisyon boyutu hesaplama
        
        Args:
            win_rate: Kazanç oranı (0-1)
            avg_win: Ortalama kazanç
            avg_loss: Ortalama kayıp
            
        Returns:
            Optimal pozisyon oranı (0-1)
        """
        if avg_loss <= 0 or win_rate <= 0:
            return 0.1  # Güvenli default değer
            
        win_loss_ratio = avg_win / abs(avg_loss)
        kelly_fraction = (win_rate * win_loss_ratio - (1 - win_rate)) / win_loss_ratio
        
        # Kelly fraction'ı güvenli sınırlar içinde tut
        return max(0.01, min(0.25, kelly_fraction))
    
    def fixed_fractional(self, portfolio_value: float, risk_percent: float) -> float:
        """
        Fixed Fractional pozisyon boyutlandırma
        
        Args:
            portfolio_value: Portföy değeri
            risk_percent: Risk yüzdesi
            
        Returns:
            Pozisyon büyüklüğü
        """
        return portfolio_value * risk_percent
    
    def volatility_based(self, portfolio_value: float, volatility: float, risk_reward: float = 1.0) -> float:
        """
        Volatiliteye dayalı pozisyon boyutlandırma
        
        Args:
            portfolio_value: Portföy değeri
            volatility: Varlık volatilitesi
            risk_reward: Risk/ödül oranı
            
        Returns:
            Pozisyon büyüklüğü
        """
        # Volatilite yüksekse pozisyonu küçült
        volatility_adjusted_risk = self.risk_config.max_position_risk / (1 + volatility)
        
        base_position = portfolio_value * volatility_adjusted_risk
        
        # Risk/ödül oranına göre ayarla
        return base_position * risk_reward
    
    def martingale_adaptive(self, previous_loss: float, base_size: float, max_multiplier: float = 3.0) -> float:
        """
        Adaptif Martingale stratejisi (dikkatli kullanım!)
        
        Args:
            previous_loss: Önceki kayıp
            base_size: Temel boyut
            max_multiplier: Maksimum çarpan
            
        Returns:
            Yeni pozisyon büyüklüğü
        """
        if previous_loss <= 0:
            return base_size
            
        multiplier = min(max_multiplier, 1 + abs(previous_loss) / base_size)
        return base_size * multiplier
    
    def calculate_position_size(self, 
                              symbol: str,
                              entry_price: float,
                              stop_loss: float,
                              portfolio_value: float,
                              strategy_type: str = "fixed_fractional",
                              **kwargs) -> Dict:
        """
        Ana pozisyon boyutlandırma fonksiyonu
        
        Args:
            symbol: Trading sembolü
            entry_price: Giriş fiyatı
            stop_loss: Stop loss fiyatı
            portfolio_value: Mevcut portföy değeri
            strategy_type: Strateji tipi
            **kwargs: Ek parametreler
            
        Returns:
            Pozisyon boyutlandırma sonuçları
        """
        
        # Risk hesaplaması
        risk_per_unit = abs(entry_price - stop_loss)
        if risk_per_unit <= 0:
            logger.warning(f"Geçersiz stop loss fiyatı: {stop_loss}")
            return {"size": 0, "risk_amount": 0, "reason": "Invalid stop loss"}
        
        portfolio_risk = risk_per_unit / portfolio_value
        
        # Portfolio risk limitini kontrol et
        if portfolio_risk > self.risk_config.max_portfolio_risk:
            logger.warning(f"Portfolio risk limiti aşıldı: {portfolio_risk:.4f} > {self.risk_config.max_portfolio_risk}")
            adjusted_position = portfolio_value * self.risk_config.max_portfolio_risk / risk_per_unit
        else:
            # Strateji tipine göre pozisyon hesapla
            if strategy_type == "kelly":
                win_rate = kwargs.get("win_rate", 0.6)
                avg_win = kwargs.get("avg_win", 0.02)
                avg_loss = kwargs.get("avg_loss", 0.01)
                risk_percent = self.kelly_criterion(win_rate, avg_win, avg_loss)
                
            elif strategy_type == "volatility":
                volatility = kwargs.get("volatility", 0.02)
                risk_reward = kwargs.get("risk_reward", 1.0)
                risk_percent = self.volatility_based(portfolio_value, volatility, risk_reward) / portfolio_value
                
            elif strategy_type == "martingale":
                previous_loss = kwargs.get("previous_loss", 0)
                base_size = portfolio_value * self.risk_config.max_position_risk
                adjusted_position = self.martingale_adaptive(previous_loss, base_size)
                risk_amount = adjusted_position * risk_per_unit
                
                return {
                    "size": adjusted_position,
                    "risk_amount": risk_amount,
                    "portfolio_risk_pct": risk_amount / portfolio_value,
                    "strategy": "martingale",
                    "reason": "Martingale adaptive"
                }
                
            else:  # fixed_fractional default
                risk_percent = self.risk_config.max_position_risk
            
            adjusted_position = portfolio_value * risk_percent / risk_per_unit
        
        # Limitleri kontrol et
        if adjusted_position < self.risk_config.min_trade_size:
            logger.info(f"Pozisyon minimum limitin altında: {adjusted_position:.2f} < {self.risk_config.min_trade_size}")
            return {"size": 0, "risk_amount": 0, "reason": "Below minimum trade size"}
        
        if adjusted_position > self.risk_config.max_trade_size:
            adjusted_position = self.risk_config.max_trade_size
            logger.info(f"Pozisyon maksimum limite ayarlandı: {adjusted_position}")
        
        risk_amount = adjusted_position * risk_per_unit
        
        result = {
            "size": adjusted_position,
            "risk_amount": risk_amount,
            "portfolio_risk_pct": risk_amount / portfolio_value,
            "strategy": strategy_type,
            "entry_price": entry_price,
            "stop_loss": stop_loss,
            "risk_per_unit": risk_per_unit,
            "reason": f"Position calculated with {strategy_type} strategy"
        }
        
        logger.info(f"Position size calculated for {symbol}: {adjusted_position:.2f} USDT")
        return result
    
    def update_position_history(self, position_data: Dict):
        """Pozisyon geçmişini güncelle"""
        self.position_history.append(position_data)
        
        # Son 100 pozisyonu tut
        if len(self.position_history) > 100:
            self.position_history = self.position_history[-100:]
    
    def get_position_statistics(self) -> Dict:
        """Pozisyon istatistikleri"""
        if not self.position_history:
            return {}
            
        sizes = [p.get("size", 0) for p in self.position_history]
        risk_amounts = [p.get("risk_amount", 0) for p in self.position_history]
        
        return {
            "total_positions": len(self.position_history),
            "avg_position_size": np.mean(sizes),
            "max_position_size": np.max(sizes),
            "min_position_size": np.min(sizes),
            "avg_risk_amount": np.mean(risk_amounts),
            "total_risk_amount": np.sum(risk_amounts)
        }

# Örnek kullanım
if __name__ == "__main__":
    # Test
    sizer = PositionSizer()
    
    result = sizer.calculate_position_size(
        symbol="BTCUSDT",
        entry_price=50000,
        stop_loss=48000,
        portfolio_value=10000,
        strategy_type="fixed_fractional"
    )
    
    print("Position Sizing Result:")
    print(result)