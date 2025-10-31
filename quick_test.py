#!/usr/bin/env python3
"""
Hızlı Sistem Testi
"""

print("🚀 Crypto Trading System - Hızlı Test")
print("=" * 40)

# 1. Python sürüm kontrolü
import sys
print(f"✅ Python sürüm: {sys.version}")

# 2. Gerekli kütüphaneleri test et
print("\n📦 Kütüphane Testleri:")
try:
    import numpy as np
    print(f"✅ NumPy: {np.__version__}")
except ImportError as e:
    print(f"❌ NumPy: {e}")

try:
    import pandas as pd
    print(f"✅ Pandas: {pd.__version__}")
except ImportError as e:
    print(f"❌ Pandas: {e}")

try:
    import ccxt
    print(f"✅ CCXT: {ccxt.__version__}")
except ImportError as e:
    print(f"❌ CCXT: {e}")

try:
    import matplotlib.pyplot as plt
    print("✅ Matplotlib: Yüklü")
except ImportError as e:
    print(f"❌ Matplotlib: {e}")

try:
    import requests
    print("✅ Requests: Yüklü")
except ImportError as e:
    print(f"❌ Requests: {e}")

try:
    from dotenv import load_dotenv
    print("✅ Python-dotenv: Yüklü")
except ImportError as e:
    print(f"❌ Python-dotenv: {e}")

# 3. Position Sizer modülü test et
print("\n🎯 Position Sizer Testi:")
try:
    from position_sizing import PositionSizer, RiskConfig
    print("✅ Position Sizer modülü başarıyla import edildi!")
    
    # Test objesi oluştur
    sizer = PositionSizer()
    
    # Basit test
    test_result = sizer.calculate_position_size(
        symbol="BTCUSDT",
        entry_price=45000,
        stop_loss=43000,
        portfolio_value=5000,
        strategy_type="fixed_fractional"
    )
    
    print(f"✅ Test pozisyonu: {test_result['size']:.2f} USDT")
    print(f"✅ Risk: %{test_result['portfolio_risk_p_pct']:.1f}")
    
except ImportError as e:
    print(f"❌ Position Sizer: {e}")
except Exception as e:
    print(f"❌ Test hatası: {e}")

print("\n" + "=" * 40)
print("🎉 Hızlı test tamamlandı!")