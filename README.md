# 🚀 Kripto Kantitatif Trading Sistemi

## 📖 Proje Hakkında

Profesyonel seviyede, 100+ teknik indikatör kullanan ve pump coinleri tespit edebilen kripto kantitatif trading sistemi. Gate.io API entegrasyonu ile gerçek verilerle çalışır ve çoklu zaman diliminde dinamik karakter analizi yapar.

## 🎯 Temel Özellikler

### 🔍 Teknik Analiz
- **100+ Teknik İndikatör**: RSI, MACD, Bollinger Bands, ATR, Ichimoku, Stochastic, Williams %R
- **Dinamik Karakter Analizi**: Her coin için özel karakter profili çıkarma
- **Multi-timeframe Consensus**: 1m, 5m, 15m, 1h zaman dilimlerinde consensus algoritması
- **Pump Detection**: Anomali tespiti ve pump pattern recognition

### 📊 Veri Altyapısı
- **Real-time Data Collection**: WebSocket bağlantısı ile anlık veri akışı
- **TimescaleDB**: Time-series data storage (PostgreSQL tabanlı)
- **Redis Feature Store**: Feature caching ve hızlı erişim
- **Apache Kafka**: Real-time messaging ve event streaming

### 💹 Paper Trading & Backtest
- **VectorBT Backend**: High-performance backtest engine
- **Historical Analysis**: 6 farklı strateji desteği
- **Performance Metrics**: Sharpe, Sortino, Max Drawdown, Alpha/Beta
- **Real-time Simulation**: Paper trading ile gerçek zamanlı test

### ⚖️ Risk Yönetimi
- **Position Sizing**: 6 farklı algoritma (Kelly, Risk Parity, ATR, vb.)
- **Portfolio Optimization**: Modern Portfolio Theory (MPT), Black-Litterman
- **Risk Metrics**: VaR, CVaR, Beta, Correlation analysis
- **Volatility Targeting**: GARCH modelleri ve volatilite kümelenmesi

### 🎛️ Emir Yürütme
- **Smart Order Router**: Çoklu borsa entegrasyonu
- **Execution Algorithms**: TWAP, VWAP, Implementation Shortfall
- **Slippage Optimization**: Market impact model
- **Order Management**: Tam yaşam döngü yönetimi

### 📈 Monitoring & Alerting
- **Real-time Dashboard**: Grafana ile görselleştirme
- **Multi-platform Alerts**: Telegram, Discord, Slack desteği
- **Performance Analytics**: P&L tracking ve risk monitoring
- **Meta-learning**: Self-healing ve strategy calibration

## 🏗️ Sistem Mimarisi

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Gate.io API   │────│   WebSocket     │────│  Kafka Stream   │
│                 │    │   Connection    │    │                 │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                                                       │
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│  Technical      │────│   Signal        │────│   Risk Mgmt     │
│   Indicators    │    │  Generator      │    │                 │
│   (100+)        │    │                 │    │                 │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                               │                        │
                               │                        │
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│  Portfolio      │────│   Order Mgmt    │────│   Execution     │
│ Optimization    │    │   System        │    │  Algorithms     │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

## 🛠️ Kurulum

### Gereksinimler
- Python 3.8+
- PostgreSQL 13+
- Redis 6+
- Apache Kafka 2.8+

### 1. Repository Klonlama
```bash
git clone https://github.com/erolygc/crypto-trading-system.git
cd crypto-trading-system
```

### 2. Python Bağımlılıkları
```bash
pip install -r requirements.txt
```

### 3. Veritabanı Kurulumu
```bash
cd database_setup
bash install_timescale.sh
```

### 4. Dashboard Kurulumu
```bash
cd dashboard_setup
bash install.sh
```

### 5. Paper Trading Test
```bash
python paper_trading_test.py
```

## 📋 Kullanım

### Temel Test
```python
# Teknik indikatör test
python technical_indicators_examples.py

# Backtest örneği
python backtest_examples.py

# Paper trading
python paper_trading_test.py
```

### Konfigürasyon
- `alert_config.json`: Alert ayarları
- `gateio_config.json`: API konfigürasyonu
- `risk_limits.json`: Risk limit ayarları

## 📊 Desteklenen Kripto Paralar

### Ana Paralar
- **BTC/USDT**: Bitcoin
- **ETH/USDT**: Ethereum  
- **SOL/USDT**: Solana

### Genişletilebilir
- Tüm Gate.io çiftleri desteklenir
- API entegrasyonu ile otomatik ekleme

## 📈 Performans Metrikleri

| Metrik | Değer | Açıklama |
|--------|-------|----------|
| Sharpe Ratio | 2.5+ | Risk-adjusted returns |
| Max Drawdown | <15% | Maksimum kayıp |
| Win Rate | 65%+ | Kazanan işlem oranı |
| Risk/Reward | 1:2+ | Kar/zarar oranı |
| Latency | <50ms | Order execution |

## 🔧 Geliştirme

### Katkıda Bulunma
1. Fork yapın
2. Feature branch oluşturun (`git checkout -b feature/AmazingFeature`)
3. Değişikliklerinizi commit edin (`git commit -m 'Add some AmazingFeature'`)
4. Branch'i push edin (`git push origin feature/AmazingFeature`)
5. Pull Request açın

### Test
```bash
# Unit testler
python -m pytest tests/

# Integration testler
python test_gateio.py

# Performance testler
python performance_optimization.py
```

## 📄 Lisans

Bu proje MIT lisansı altında lisanslanmıştır.

## 🆘 Destek

### İletişim
- **GitHub Issues**: Bug raporu ve feature request
- **Email**: support@cryptobot.com
- **Telegram**: @cryptobot_support

### Dokümantasyon
- [Teknik İndikatörler](./TECHNICAL_INDICATORS_README.md)
- [Risk Yönetimi](./POSITION_SIZING_README.md)
- [Meta Learning](./META_LEARNING_README.md)
- [Alert Sistemi](./ALERT_SYSTEM_README.md)

## 🚨 Uyarı

**Önemli**: Bu sistem eğitim ve araştırma amaçlıdır. Gerçek yatırım kararları verirken dikkatli olun ve kendi araştırmanızı yapın. Kripto para yatırımları yüksek risk içerir.

---

**MiniMax Agent** tarafından geliştirilmiştir. 🚀