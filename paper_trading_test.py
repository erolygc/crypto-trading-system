#!/usr/bin/env python3
"""
Paper Trading Test Script
Simülasyon ortamında trading sistemini test et
"""

import sys
import os
import time
from typing import Dict, List, Tuple
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import matplotlib.pyplot as plt

# Add current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Import custom modules
try:
    from position_sizing import PositionSizer, RiskConfig
    print("✅ Position Sizer modülü yüklendi")
except ImportError as e:
    print(f"❌ Position Sizer yüklenemedi: {e}")
    sys.exit(1)

# Try to import trading modules
try:
    from signal_generator import SignalGenerator
    print("✅ Signal Generator yüklendi")
    signal_gen_available = True
except ImportError:
    print("⚠️ Signal Generator bulunamadı - basit sinyaller kullanılacak")
    signal_gen_available = False

class PaperTrader:
    """
    Kağıt Trading Simülatörü
    """
    
    def __init__(self, initial_balance: float = 10000):
        self.initial_balance = initial_balance
        self.balance = initial_balance
        self.positions = []
        self.trades = []
        self.pnl_history = []
        self.position_sizer = PositionSizer()
        
    def calculate_portfolio_value(self, current_prices: Dict[str, float]) -> float:
        """Mevcut portföy değerini hesapla"""
        total_value = self.balance
        
        for position in self.positions:
            symbol = position['symbol']
            size = position['size']
            entry_price = position['entry_price']
            
            if symbol in current_prices:
                current_value = size * current_prices[symbol]
                entry_value = size * entry_price
                unrealized_pnl = current_value - entry_value
                total_value += unrealized_pnl
                
        return total_value
    
    def open_position(self, symbol: str, entry_price: float, size: float, 
                     stop_loss: float, strategy_type: str = "fixed_fractional") -> bool:
        """Yeni pozisyon aç"""
        if size > self.balance:
            return False
            
        position = {
            'symbol': symbol,
            'size': size,
            'entry_price': entry_price,
            'stop_loss': stop_loss,
            'strategy': strategy_type,
            'timestamp': datetime.now()
        }
        
        self.positions.append(position)
        self.balance -= size
        
        print(f"📈 Pozisyon açıldı: {symbol} - {size:.2f} @ {entry_price}")
        return True
    
    def close_position(self, position: dict, exit_price: float, reason: str = "Exit") -> float:
        """Pozisyonu kapat"""
        size = position['size']
        entry_price = position['entry_price']
        symbol = position['symbol']
        
        pnl = (exit_price - entry_price) * size
        
        # Trade kaydı
        trade = {
            'symbol': symbol,
            'size': size,
            'entry_price': entry_price,
            'exit_price': exit_price,
            'pnl': pnl,
            'reason': reason,
            'timestamp': datetime.now()
        }
        
        self.trades.append(trade)
        self.balance += size + pnl
        
        print(f"📉 Pozisyon kapandı: {symbol} - PnL: {pnl:.2f} ({reason})")
        return pnl
    
    def check_stop_losses(self, current_prices: Dict[str, float]) -> List[dict]:
        """Stop loss kontrolü"""
        closed_positions = []
        
        for position in self.positions[:]:  # Liste üzerinde iterasyon
            symbol = position['symbol']
            stop_loss = position['stop_loss']
            
            if symbol in current_prices:
                current_price = current_prices[symbol]
                
                # Long pozisyon için stop loss kontrolü
                if current_price <= stop_loss:
                    closed_positions.append((position, current_price, "Stop Loss"))
                    self.positions.remove(position)
                    
        return closed_positions
    
    def generate_simple_signal(self, df: pd.DataFrame) -> str:
        """Basit sinyal üreteci (MA crossover)"""
        if len(df) < 20:
            return "HOLD"
            
        # 5 ve 20 periodluk MA
        df['MA5'] = df['close'].rolling(5).mean()
        df['MA20'] = df['close'].rolling(20).mean()
        
        if pd.isna(df['MA5'].iloc[-1]) or pd.isna(df['MA20'].iloc[-1]):
            return "HOLD"
            
        # Golden Cross: MA5, MA20'yi yukarı kesiyor
        if df['MA5'].iloc[-2] <= df['MA20'].iloc[-2] and df['MA5'].iloc[-1] > df['MA20'].iloc[-1]:
            return "BUY"
            
        # Death Cross: MA5, MA20'yi aşağı kesiyor  
        if df['MA5'].iloc[-2] >= df['MA20'].iloc[-2] and df['MA5'].iloc[-1] < df['MA20'].iloc[-1]:
            return "SELL"
            
        return "HOLD"
    
    def start_simulation(self, data: Dict[str, pd.DataFrame], duration_days: int = 7):
        """Simülasyon başlat"""
        print(f"🚀 Paper Trading Simülasyonu Başlıyor...")
        print(f"📊 Süre: {duration_days} gün")
        print(f"💰 Başlangıç Bakiyesi: ${self.initial_balance:.2f}")
        print("=" * 50)
        
        start_date = datetime.now()
        
        for day in range(duration_days):
            print(f"\n📅 Gün {day + 1} - {start_date + timedelta(days=day):%Y-%m-%d}")
            
            # Her sembol için işlem kontrolü
            for symbol, df in data.items():
                if len(df) == 0:
                    continue
                    
                current_price = df['close'].iloc[-1]
                
                # Sinyal üret
                signal = self.generate_simple_signal(df)
                
                # Pozisyon yönetimi
                existing_position = next((p for p in self.positions if p['symbol'] == symbol), None)
                
                if signal == "BUY" and not existing_position:
                    # Yeni pozisyon aç
                    entry_price = current_price
                    stop_loss = entry_price * 0.95  # %5 stop loss
                    
                    position_size = self.position_sizer.calculate_position_size(
                        symbol=symbol,
                        entry_price=entry_price,
                        stop_loss=stop_loss,
                        portfolio_value=self.balance,
                        strategy_type="fixed_fractional"
                    )
                    
                    if position_size['size'] > 0:
                        self.open_position(symbol, entry_price, position_size['size'], stop_loss)
                        
                elif signal == "SELL" and existing_position:
                    # Pozisyon kapat
                    self.close_position(existing_position, current_price, "Signal Exit")
            
            # Stop loss kontrolü
            current_prices = {symbol: df['close'].iloc[-1] for symbol, df in data.items() if len(df) > 0}
            closed = self.check_stop_losses(current_prices)
            
            for position, exit_price, reason in closed:
                self.close_position(position, exit_price, reason)
            
            # Portföy durumu
            portfolio_value = self.calculate_portfolio_value(current_prices)
            daily_pnl = portfolio_value - (self.initial_balance + sum([t['pnl'] for t in self.trades]))
            
            self.pnl_history.append({
                'date': start_date + timedelta(days=day),
                'portfolio_value': portfolio_value,
                'daily_pnl': daily_pnl,
                'balance': self.balance
            })
            
            print(f"💼 Portföy Değeri: ${portfolio_value:.2f}")
            print(f"📈 Günlük P&L: ${daily_pnl:.2f}")
            print(f"💵 Mevcut Bakiye: ${self.balance:.2f}")
            print(f"📊 Aktif Pozisyonlar: {len(self.positions)}")
    
    def generate_report(self) -> str:
        """Simülasyon raporu üret"""
        if not self.pnl_history:
            return "Henüz simülasyon yapılmadı."
            
        final_value = self.pnl_history[-1]['portfolio_value']
        total_return = ((final_value - self.initial_balance) / self.initial_balance) * 100
        
        winning_trades = [t for t in self.trades if t['pnl'] > 0]
        losing_trades = [t for t in self.trades if t['pnl'] < 0]
        
        win_rate = len(winning_trades) / len(self.trades) * 100 if self.trades else 0
        
        report = f"""
📊 PAPER TRADING SİMÜLASYONU RAPORU
=====================================
💰 Başlangıç Bakiyesi: ${self.initial_balance:.2f}
📈 Final Portföy Değeri: ${final_value:.2f}
🎯 Toplam Getiri: {total_return:.2f}%

📈 İŞLEM İSTATİSTİKLERİ:
• Toplam İşlem: {len(self.trades)}
• Kazanan İşlem: {len(winning_trades)}
• Kaybeden İşlem: {len(losing_trades)}
• Başarı Oranı: {win_rate:.1f}%

💵 KAR/ZARAR DETAYLARI:
• Toplam Kar: ${sum([t['pnl'] for t in winning_trades]):.2f}
• Toplam Zarar: ${sum([t['pnl'] for t in losing_trades]):.2f}
• Net P&L: ${sum([t['pnl'] for t in self.trades]):.2f}

🎲 ORTALAMA İŞLEM:
• Ortalama Kazanç: ${np.mean([t['pnl'] for t in winning_trades]):.2f} (Kazanan)
• Ortalama Kayıp: ${np.mean([t['pnl'] for t in losing_trades]):.2f} (Kaybeden)
"""
        
        if self.trades:
            best_trade = max(self.trades, key=lambda x: x['pnl'])
            worst_trade = min(self.trades, key=lambda x: x['pnl'])
            
            report += f"""
🏆 EN İYİ İŞLEM:
• {best_trade['symbol']}: ${best_trade['pnl']:.2f} (Exit: {best_trade['reason']})

💸 EN KÖTÜ İŞLEM:
• {worst_trade['symbol']}: ${worst_trade['pnl']:.2f} (Exit: {worst_trade['reason']})
"""
        
        return report
    
    def plot_performance(self, save_path: str = "paper_trading_results.png"):
        """Performans grafiği çiz"""
        if not self.pnl_history:
            print("Performans verisi bulunamadı.")
            return
            
        plt.figure(figsize=(12, 8))
        
        dates = [p['date'] for p in self.pnl_history]
        portfolio_values = [p['portfolio_value'] for p in self.pnl_history]
        balances = [p['balance'] for p in self.pnl_history]
        
        # Portföy değeri grafiği
        plt.subplot(2, 1, 1)
        plt.plot(dates, portfolio_values, label='Portföy Değeri', linewidth=2)
        plt.axhline(y=self.initial_balance, color='r', linestyle='--', label='Başlangıç')
        plt.title('Paper Trading - Portföy Değeri')
        plt.ylabel('Değer ($)')
        plt.legend()
        plt.grid(True)
        
        # Günlük P&L grafiği
        plt.subplot(2, 1, 2)
        daily_pnls = [p['daily_pnl'] for p in self.pnl_history]
        colors = ['green' if pnl >= 0 else 'red' for pnl in daily_pnls]
        plt.bar(dates, daily_pnls, color=colors, alpha=0.7)
        plt.title('Günlük P&L')
        plt.ylabel('P&L ($)')
        plt.xlabel('Tarih')
        plt.grid(True, alpha=0.3)
        
        plt.tight_layout()
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"📈 Performans grafiği kaydedildi: {save_path}")
        plt.show()

def create_sample_data(symbols: List[str], days: int = 30) -> Dict[str, pd.DataFrame]:
    """Örnek veri üret (test için)"""
    np.random.seed(42)  # Sabit sonuçlar için
    data = {}
    
    for symbol in symbols:
        dates = pd.date_range(start=datetime.now() - timedelta(days=days), 
                             end=datetime.now(), freq='H')
        
        # Rastgele fiyat hareketi simülasyonu
        returns = np.random.normal(0, 0.02, len(dates))
        prices = [50000]  # Başlangıç fiyatı (BTC için)
        
        for i in range(1, len(dates)):
            new_price = prices[-1] * (1 + returns[i])
            prices.append(new_price)
        
        # DataFrame oluştur
        df = pd.DataFrame({
            'timestamp': dates,
            'open': prices,
            'high': [p * 1.01 for p in prices],
            'low': [p * 0.99 for p in prices],
            'close': prices,
            'volume': np.random.uniform(100, 1000, len(dates))
        })
        
        data[symbol] = df
        
    return data

def main():
    """Ana test fonksiyonu"""
    print("🚀 Paper Trading Test Sistemi")
    print("=" * 40)
    
    # Test verileri oluştur
    test_symbols = ['BTCUSDT', 'ETHUSDT', 'BNBUSDT']
    data = create_sample_data(test_symbols, days=14)
    
    print(f"📊 Test verileri oluşturuldu: {len(test_symbols)} sembol")
    
    # Paper trader oluştur
    trader = PaperTrader(initial_balance=10000)
    
    # Simülasyon başlat
    trader.start_simulation(data, duration_days=7)
    
    # Rapor üret
    print("\n" + "=" * 50)
    print(trader.generate_report())
    
    # Performans grafiği
    try:
        trader.plot_performance()
    except Exception as e:
        print(f"⚠️ Grafik oluşturulamadı: {e}")
    
    print("\n✅ Paper Trading testi tamamlandı!")

if __name__ == "__main__":
    main()