# Teknik İndikatörler Dokümantasyonu

## Genel Bakış

Bu sistem 100+ teknik indikatörü destekleyen kapsamlı bir teknik analiz paketi sunar.

## Ana İndikatörler

### Trend İndikatörleri
- **SMA**: Simple Moving Average
- **EMA**: Exponential Moving Average
- **MACD**: Moving Average Convergence Divergence
- **ADX**: Average Directional Index
- **Parabolic SAR**: Stop and Reverse

### Momentum İndikatörleri
- **RSI**: Relative Strength Index
- **Stochastic Oscillator**
- **Williams %R**
- **CCI**: Commodity Channel Index
- **ROC**: Rate of Change

### Volatilite İndikatörleri
- **Bollinger Bands**
- **Average True Range (ATR)**
- **Keltner Channels**
- **Donchian Channels**

### Hacim İndikatörleri
- **Volume Weighted Average Price (VWAP)**
- **Accumulation/Distribution Line**
- **On Balance Volume (OBV)**
- **Chaikin Money Flow**

## Kullanım Örnekleri

```python
from technical_indicators import TechnicalIndicators
import pandas as pd

# İndikatör sistemi başlat
ti = TechnicalIndicators()

# Fiyat verisi (örnek)
prices = pd.Series([100, 102, 101, 105, 103, 107, 110])

# RSI hesapla
rsi = ti.rsi(prices, period=14)
print(f"RSI: {rsi.iloc[-1]:.2f}")

# MACD hesapla
macd_data = ti.macd(prices)
print(f"MACD Signal: {macd_data['signal'].iloc[-1]:.4f}")

# Bollinger Bands
bb = ti.bollinger_bands(prices)
current_price = prices.iloc[-1]
if current_price > bb['upper'].iloc[-1]:
    print("Fiyat üst bant üzerinde - Sat sinyali")
elif current_price < bb['lower'].iloc[-1]:
    print("Fiyat alt bant altında - Al sinyali")
else:
    print("Fiyat bantlar arasında - Nötr")
```

## Parametreler

### RSI
- **period**: Hesaplama periyodu (varsayılan: 14)
- **overbought**: Aşırı alım seviyesi (varsayılan: 70)
- **oversold**: Aşırı satım seviyesi (varsayılan: 30)

### MACD
- **fast**: Hızlı EMA periyodu (varsayılan: 12)
- **slow**: Yavaş EMA periyodu (varsayılan: 26)
- **signal**: Signal line periyodu (varsayılan: 9)

### Bollinger Bands
- **period**: Moving average periyodu (varsayılan: 20)
- **std_dev**: Standart sapma çarpanı (varsayılan: 2)

## Performans Optimizasyonu

- **Vectorized Operations**: NumPy vectorization kullanır
- **Memory Efficient**: Rolling window optimizasyonu
- **Parallel Processing**: Multi-threading desteği
- **Caching**: Computed values cache'lenir

## Uyarılar

1. Yeterli veri olmadan indikatörler yanıltıcı olabilir
2. Geçmiş performans gelecekteki sonuçları garanti etmez
3. Tek başına indikatörler yeterli değildir, kombinasyon kullanın
4. Risk yönetimi her zaman öncelikli olmalıdır

## Lisans

MIT License
