"""
Crypto Trading System - Quick Test
VS Code'da hızlı test için basit script
"""

import sys
import os

# Add current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_imports():
    """Temel import testleri"""
    try:
        import numpy as np
        import pandas as pd
        import talib
        print("✅ Temel kütüphaneler başarıyla import edildi")
        return True
    except ImportError as e:
        print(f"❌ Import hatası: {e}")
        return False

def test_position_sizing():
    """Position sizing modülü testi"""
    try:
        from position_sizing import PositionSizer, RiskConfig
        
        sizer = PositionSizer()
        result = sizer.calculate_position_size(
            symbol="BTCUSDT",
            entry_price=50000,
            stop_loss=48000,
            portfolio_value=10000,
            strategy_type="fixed_fractional"
        )
        
        print("✅ Position Sizing çalışıyor")
        print(f"📊 Hesaplanan pozisyon büyüklüğü: {result['size']:.2f} USDT")
        return True
    except Exception as e:
        print(f"❌ Position Sizing hatası: {e}")
        return False

def main():
    """Ana test fonksiyonu"""
    print("🚀 Crypto Trading System - Quick Test")
    print("=" * 50)
    
    # Test imports
    if not test_imports():
        print("\n⚠️  Lütfen önce bağımlılıkları yükleyin:")
        print("pip install -r requirements-fixed.txt")
        return
    
    print("\n" + "-" * 30)
    
    # Test position sizing
    test_position_sizing()
    
    print("\n" + "=" * 50)
    print("✅ Test tamamlandı!")

if __name__ == "__main__":
    main()