#!/usr/bin/env python3
"""
Position Sizer - Detaylı Test Script
"""

def main():
    from position_sizing import PositionSizer, RiskConfig
    
    print("🚀 Position Sizer - Detaylı Test")
    print("=" * 50)
    
    # Sizer oluştur
    sizer = PositionSizer()
    
    # Test 1: Fixed Fractional Strategy
    print("\n📊 Test 1: Fixed Fractional Strateji")
    result1 = sizer.calculate_position_size(
        symbol="BTCUSDT",
        entry_price=45000,
        stop_loss=43000,
        portfolio_value=5000,  # 5 USDT'lik portföy
        strategy_type="fixed_fractional"
    )
    print(f"Pozisyon: {result1['size']:.2f} USDT")
    print(f"Risk: {result1['portfolio_risk_pct']:.2%}")
    print(f"Neden: {result1['reason']}")
    
    # Test 2: Kelly Criterion Strategy
    print("\n🧠 Test 2: Kelly Criterion Strateji")
    result2 = sizer.calculate_position_size(
        symbol="ETHUSDT",
        entry_price=3000,
        stop_loss=2800,
        portfolio_value=10000,
        strategy_type="kelly",
        win_rate=0.65,  # %65 kazanma oranı
        avg_win=0.03,   # %3 ortalama kazanç
        avg_loss=0.02   # %2 ortalama kayıp
    )
    print(f"Pozisyon: {result2['size']:.2f} USDT")
    print(f"Risk: {result2['portfolio_risk_pct']:.2%}")
    print(f"Neden: {result2['reason']}")
    
    # Test 3: Volatility-based Strategy
    print("\n📈 Test 3: Volatility-based Strateji")
    result3 = sizer.calculate_position_size(
        symbol="BNBUSDT",
        entry_price=200,
        stop_loss=180,
        portfolio_value=8000,
        strategy_type="volatility",
        volatility=0.04,     # %4 volatilite
        risk_reward=1.5      # 1.5 risk/ödül
    )
    print(f"Pozisyon: {result3['size']:.2f} USDT")
    print(f"Risk: {result3['portfolio_risk_pct']:.2%}")
    print(f"Neden: {result3['reason']}")
    
    # Test 4: Risk Configuration Test
    print("\n⚙️ Test 4: Özelleştirilmiş Risk Konfigürasyonu")
    custom_config = RiskConfig(
        max_position_risk=0.015,  # %1.5 pozisyon riski
        max_portfolio_risk=0.03   # %3 portföy riski
    )
    custom_sizer = PositionSizer(custom_config)
    
    result4 = custom_sizer.calculate_position_size(
        symbol="ADAUSDT",
        entry_price=1.0,
        stop_loss=0.9,
        portfolio_value=2000,
        strategy_type="fixed_fractional"
    )
    print(f"Pozisyon: {result4['size']:.2f} USDT")
    print(f"Risk: {result4['portfolio_risk_pct']:.2%}")
    print(f"Neden: {result4['reason']}")
    
    print("\n" + "=" * 50)
    print("✅ Tüm Position Sizer testleri tamamlandı!")
    
    # Summary
    print("\n📋 Test Özeti:")
    print(f"1. Fixed Fractional: {result1['size']:.2f} USDT")
    print(f"2. Kelly Criterion: {result2['size']:.2f} USDT")
    print(f"3. Volatility-based: {result3['size']:.2f} USDT")
    print(f"4. Custom Risk: {result4['size']:.2f} USDT")

if __name__ == "__main__":
    main()