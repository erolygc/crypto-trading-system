#!/usr/bin/env python3
"""
Position Sizer - Güvenli Test Script
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
        return max(0.01, min(kelly_fraction, 0.25))  # %1 ile %25 arası
    
    def fixed_fractional(self, risk_per_trade: float) -> float:
        """
        Fixed Fractional position sizing
        
        Args:
            risk_per_trade: İşlem başına risk oranı (0-1)
            
        Returns:
            Pozisyon oranı (0-1)
        """
        return max(0.01, min(risk_per_trade, self.risk_config.max_position_risk))
    
    def volatility_based(self, volatility: float, risk_reward_ratio: float) -> float:
        """
        Volatiliteye göre pozisyon boyutu
        
        Args:
            volatility: Varlık volatilitesi (0-1)
            risk_reward_ratio: Risk/ödül oranı
            
        Returns:
            Pozisyon oranı (0-1)
        """
        # Volatilite arttıkça pozisyon boyutu azalır
        if volatility <= 0:
            return 0.1
            
        # Volatiliteye göre risk ayarlaması
        volatility_adjustment = 1 / (volatility * 10)  # Volatilite faktörü
        base_risk = self.risk_config.max_position_risk / volatility_adjustment
        
        # Risk/ödül oranına göre ayarlama
        if risk_reward_ratio < 1:
            base_risk *= 0.5  # Düşük R/R için daha az risk
            
        return max(0.01, min(base_risk, self.risk_config.max_position_risk))
    
    def martingale(self, consecutive_losses: int, base_risk: float) -> float:
        """
        Martingale position sizing (DİKKAT: Yüksek risk!)
        
        Args:
            consecutive_losses: Art arda kayıp sayısı
            base_risk: Temel risk oranı
            
        Returns:
            Pozisyon oranı (0-1)
        """
        # Maksimum 3 kat artış
        multiplier = min(2 ** min(consecutive_losses, 3), 8)
        adjusted_risk = min(base_risk * multiplier, self.risk_config.max_position_risk)
        
        return adjusted_risk
    
    def calculate_position_size(
        self,
        symbol: str,
        entry_price: float,
        stop_loss: float,
        portfolio_value: float,
        strategy_type: str = "fixed_fractional",
        **kwargs
    ) -> Dict:
        """
        Ana pozisyon boyutu hesaplama fonksiyonu
        
        Args:
            symbol: İşlem sembolü
            entry_price: Giriş fiyatı
            stop_loss: Stop loss fiyatı
            portfolio_value: Portföy değeri
            strategy_type: Kullanılacak strateji
            **kwargs: Stratejiye özel parametreler
            
        Returns:
            Hesaplama sonuçları
        """
        try:
            # Risk hesaplama
            risk_amount = abs(entry_price - stop_loss)
            if entry_price <= 0 or stop_loss <= 0:
                return {
                    "size": 0,
                    "percentage": 0,
                    "reason": "Geçersiz fiyat bilgisi",
                    "portfolio_risk_pct": 0
                }
            
            price_risk_pct = risk_amount / entry_price
            position_value = portfolio_value * self.risk_config.max_position_risk / price_risk_pct if price_risk_pct > 0 else 0
            
            # Stratejiye göre hesaplama
            if strategy_type == "kelly":
                win_rate = kwargs.get("win_rate", 0.6)
                avg_win = kwargs.get("avg_win", 0.02)
                avg_loss = kwargs.get("avg_loss", 0.01)
                kelly_fraction = self.kelly_criterion(win_rate, avg_win, avg_loss)
                
                position_size = portfolio_value * kelly_fraction
                reason = f"Kelly Criterion (W:{win_rate:.1%}, AvgWin:{avg_win:.1%})"
                
            elif strategy_type == "fixed_fractional":
                risk_pct = kwargs.get("risk_pct", 0.02)
                position_size = portfolio_value * self.fixed_fractional(risk_pct)
                reason = f"Fixed Fractional ({risk_pct:.1%} risk)"
                
            elif strategy_type == "volatility":
                volatility = kwargs.get("volatility", 0.03)
                risk_reward = kwargs.get("risk_reward", 2.0)
                position_ratio = self.volatility_based(volatility, risk_reward)
                position_size = portfolio_value * position_ratio
                reason = f"Volatility-based (Vol:{volatility:.1%}, R/R:{risk_reward:.1f})"
                
            elif strategy_type == "martingale":
                consecutive_losses = kwargs.get("consecutive_losses", 0)
                base_risk = kwargs.get("base_risk", 0.01)
                position_ratio = self.martingale(consecutive_losses, base_risk)
                position_size = portfolio_value * position_ratio
                reason = f"Martingale (Loss streak: {consecutive_losses})"
                
            else:
                # Default fixed fractional
                position_size = portfolio_value * self.risk_config.max_position_risk
                reason = "Default Fixed Fractional"
            
            # Limitler uygula
            position_size = max(
                self.risk_config.min_trade_size,
                min(position_size, self.risk_config.max_trade_size, portfolio_value)
            )
            
            # Portföy riski kontrolü
            portfolio_risk_pct = (position_size * price_risk_pct) / portfolio_value if portfolio_value > 0 else 0
            
            if portfolio_risk_pct > self.risk_config.max_portfolio_risk:
                # Risk çok yüksek, ayarla
                safe_position_size = (portfolio_value * self.risk_config.max_portfolio_risk) / price_risk_pct if price_risk_pct > 0 else 0
                position_size = min(safe_position_size, self.risk_config.max_trade_size)
                portfolio_risk_pct = (position_size * price_risk_pct) / portfolio_value if portfolio_value > 0 else 0
                reason += " (Risk adjusted)"
            
            return {
                "size": round(position_size, 2),
                "percentage": round(position_size / portfolio_value * 100, 2) if portfolio_value > 0 else 0,
                "reason": reason,
                "portfolio_risk_pct": round(portfolio_risk_pct * 100, 2),
                "price_risk_pct": round(price_risk_pct * 100, 2),
                "strategy": strategy_type
            }
            
        except Exception as e:
            logger.error(f"Position sizing hatası: {e}")
            return {
                "size": 0,
                "percentage": 0,
                "reason": f"Hata: {str(e)}",
                "portfolio_risk_pct": 0,
                "price_risk_pct": 0,
                "strategy": strategy_type
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