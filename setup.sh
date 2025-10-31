#!/bin/bash
# Crypto Trading System - Auto Setup Script
echo "🚀 Crypto Trading System - Otomatik Kurulum"
echo "============================================"

# Sanal ortam kontrolü
if [ ! -d "venv" ]; then
    echo "📦 Sanal ortam oluşturuluyor..."
    python -m venv venv
fi

echo "✅ Sanal ortam hazır"

# Sanal ortamı aktif et
source venv/bin/activate 2>/dev/null || venv\Scripts\activate 2>/dev/null

if [ $? -ne 0 ]; then
    echo "❌ Sanal ortam aktif edilemedi"
    exit 1
fi

echo "✅ Sanal ortam aktif"

# pip güncelle
echo "🔄 pip güncelleniyor..."
python -m pip install --upgrade pip

# Core packages önce kur
echo "📦 Temel paketler kuruluyor..."
pip install numpy>=1.24.0,<2.0.0
pip install pandas>=2.0.0,<3.0.0  
pip install scipy>=1.10.0,<2.0.0
pip install scikit-learn>=1.3.0,<2.0.0

# Technical analysis
echo "📊 Teknik analiz paketleri kuruluyor..."
pip install TA-Lib
pip install pandas-ta

# Trading & API
echo "💹 Trading paketleri kuruluyor..."
pip install ccxt>=4.0.0
pip install requests>=2.31.0
pip install websockets>=11.0.0

# Database & Caching
echo "🗄️  Veritabanı paketleri kuruluyor..."
pip install psycopg2-binary>=2.9.0
pip install redis>=4.5.0

# Message Queue
echo "📡 Message queue paketleri kuruluyor..."
pip install kafka-python>=2.0.2

# Visualization
echo "📈 Görselleştirme paketleri kuruluyor..."
pip install matplotlib>=3.7.0
pip install plotly>=5.15.0

# Development
echo "🔧 Geliştirme paketleri kuruluyor..."
pip install python-dotenv>=1.0.0
pip install pydantic>=2.3.0
pip install pytest>=7.4.0

echo ""
echo "✅ Tüm paketler başarıyla kuruldu!"
echo ""
echo "🧪 Sistem test ediliyor..."

# Test importları
python -c "
try:
    import numpy, pandas, talib, ccxt, requests, websockets
    print('✅ Tüm temel paketler çalışıyor!')
except ImportError as e:
    print(f'❌ Hata: {e}')
    exit(1)
"

if [ $? -eq 0 ]; then
    echo ""
    echo "🎉 Kurulum başarılı!"
    echo ""
    echo "📝 Sonraki adımlar:"
    echo "   1. .env dosyası oluşturun (API anahtarları)"
    echo "   2. python quick_test.py - Hızlı test"
    echo "   3. python paper_trading_test.py - Ana test"
fi