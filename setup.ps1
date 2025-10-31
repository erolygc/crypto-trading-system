# Crypto Trading System - Windows Kurulum Script
Write-Host "🚀 Crypto Trading System - Otomatik Kurulum (Windows)" -ForegroundColor Green
Write-Host "=" * 50 -ForegroundColor Yellow

# Sanal ortam kontrolü
if (-not (Test-Path "venv")) {
    Write-Host "📦 Sanal ortam oluşturuluyor..." -ForegroundColor Yellow
    python -m venv venv
    if ($LASTEXITCODE -ne 0) {
        Write-Host "❌ Sanal ortam oluşturulamadı!" -ForegroundColor Red
        exit 1
    }
}

Write-Host "✅ Sanal ortam hazır" -ForegroundColor Green

# Sanal ortamı aktif et
try {
    & ".\venv\Scripts\Activate.ps1"
    if ($LASTEXITCODE -ne 0) {
        Write-Host "❌ Sanal ortam aktif edilemedi!" -ForegroundColor Red
        exit 1
    }
    Write-Host "✅ Sanal ortam aktif" -ForegroundColor Green
} catch {
    Write-Host "⚠️  PowerShell script çalıştırma politikası sorunu. Manuel aktivasyon deneyin:" -ForegroundColor Yellow
    Write-Host "   .\venv\Scripts\Activate.ps1" -ForegroundColor Cyan
    Write-Host "   Sonra bu scripti tekrar çalıştırın." -ForegroundColor Yellow
    exit 1
}

# pip güncelle
Write-Host "🔄 pip güncelleniyor..." -ForegroundColor Yellow
python -m pip install --upgrade pip
if ($LASTEXITCODE -ne 0) {
    Write-Host "⚠️  pip güncellemesi atlanıyor..." -ForegroundColor Yellow
}

# Core packages önce kur
Write-Host "📦 Temel paketler kuruluyor..." -ForegroundColor Yellow
pip install "numpy>=1.24.0,<2.0.0"
if ($LASTEXITCODE -ne 0) { Write-Host "❌ numpy kurulum hatası!" -ForegroundColor Red }

pip install "pandas>=2.0.0,<3.0.0"  
if ($LASTEXITCODE -ne 0) { Write-Host "❌ pandas kurulum hatası!" -ForegroundColor Red }

pip install "scipy>=1.10.0,<2.0.0"
if ($LASTEXITCODE -ne 0) { Write-Host "❌ scipy kurulum hatası!" -ForegroundColor Red }

pip install "scikit-learn>=1.3.0,<2.0.0"
if ($LASTEXITCODE -ne 0) { Write-Host "❌ scikit-learn kurulum hatası!" -ForegroundColor Red }

# Technical analysis
Write-Host "📊 Teknik analiz paketleri kuruluyor..." -ForegroundColor Yellow
try {
    pip install TA-Lib
    if ($LASTEXITCODE -eq 0) {
        Write-Host "✅ TA-Lib kuruldu" -ForegroundColor Green
    }
} catch {
    Write-Host "⚠️  TA-Lib kurulumu atlanıyor (opsiyonel)" -ForegroundColor Yellow
}

try {
    pip install "pandas-ta>=0.3.14b0"
    if ($LASTEXITCODE -eq 0) {
        Write-Host "✅ pandas-ta kuruldu" -ForegroundColor Green
    }
} catch {
    Write-Host "⚠️  pandas-ta kurulumu atlanıyor (opsiyonel)" -ForegroundColor Yellow
}

# Trading & API
Write-Host "💹 Trading paketleri kuruluyor..." -ForegroundColor Yellow
pip install "ccxt>=4.0.0"
if ($LASTEXITCODE -ne 0) { Write-Host "❌ ccxt kurulum hatası!" -ForegroundColor Red }

pip install "requests>=2.31.0"
if ($LASTEXITCODE -ne 0) { Write-Host "❌ requests kurulum hatası!" -ForegroundColor Red }

pip install "websockets>=11.0.0"
if ($LASTEXITCODE -ne 0) { Write-Host "❌ websockets kurulum hatası!" -ForegroundColor Red }

# Database & Caching
Write-Host "🗄️  Veritabanı paketleri kuruluyor..." -ForegroundColor Yellow
try {
    pip install "psycopg2-binary>=2.9.0"
    if ($LASTEXITCODE -eq 0) {
        Write-Host "✅ psycopg2-binary kuruldu" -ForegroundColor Green
    }
} catch {
    Write-Host "⚠️  psycopg2-binary kurulumu atlanıyor (opsiyonel)" -ForegroundColor Yellow
}

try {
    pip install "redis>=4.5.0"
    if ($LASTEXITCODE -eq 0) {
        Write-Host "✅ redis kuruldu" -ForegroundColor Green
    }
} catch {
    Write-Host "⚠️  redis kurulumu atlanıyor (opsiyonel)" -ForegroundColor Yellow
}

# Message Queue
Write-Host "📡 Message queue paketleri kuruluyor..." -ForegroundColor Yellow
try {
    pip install "kafka-python>=2.0.2"
    if ($LASTEXITCODE -eq 0) {
        Write-Host "✅ kafka-python kuruldu" -ForegroundColor Green
    }
} catch {
    Write-Host "⚠️  kafka-python kurulumu atlanıyor (opsiyonel)" -ForegroundColor Yellow
}

# Visualization
Write-Host "📈 Görselleştirme paketleri kuruluyor..." -ForegroundColor Yellow
pip install "matplotlib>=3.7.0"
if ($LASTEXITCODE -ne 0) { Write-Host "❌ matplotlib kurulum hatası!" -ForegroundColor Red }

try {
    pip install "plotly>=5.15.0"
    if ($LASTEXITCODE -eq 0) {
        Write-Host "✅ plotly kuruldu" -ForegroundColor Green
    }
} catch {
    Write-Host "⚠️  plotly kurulumu atlanıyor (opsiyonel)" -ForegroundColor Yellow
}

# Development
Write-Host "🔧 Geliştirme paketleri kuruluyor..." -ForegroundColor Yellow
pip install "python-dotenv>=1.0.0"
if ($LASTEXITCODE -ne 0) { Write-Host "❌ python-dotenv kurulum hatası!" -ForegroundColor Red }

pip install "pydantic>=2.3.0"
if ($LASTEXITCODE -ne 0) { Write-Host "❌ pydantic kurulum hatası!" -ForegroundColor Red }

pip install "pytest>=7.4.0"
if ($LASTEXITCODE -ne 0) { Write-Host "❌ pytest kurulum hatası!" -ForegroundColor Red }

Write-Host "`n🧪 Sistem test ediliyor..." -ForegroundColor Yellow

# Test importları
try {
    python -c "
try:
    import numpy
    import pandas
    import requests
    import ccxt
    print('✅ Temel paketler çalışıyor!')
    
    # TA-Lib testi (opsiyonel)
    try:
        import talib
        print('✅ TA-Lib çalışıyor!')
    except ImportError:
        print('⚠️  TA-Lib bulunamadı (opsiyonel)')
        
except ImportError as e:
    print(f'❌ Hata: {e}')
    exit(1)
"
    if ($LASTEXITCODE -eq 0) {
        Write-Host "`n🎉 Kurulum başarılı!" -ForegroundColor Green
        Write-Host "`n📝 Sonraki adımlar:" -ForegroundColor Cyan
        Write-Host "   1. .env dosyası oluşturun (API anahtarları)" -ForegroundColor White
        Write-Host "   2. python quick_test.py - Hızlı test" -ForegroundColor White
        Write-Host "   3. python paper_trading_test.py - Ana test" -ForegroundColor White
    }
} catch {
    Write-Host "❌ Test başarısız!" -ForegroundColor Red
    Write-Host "Lütfen hata mesajlarını kontrol edin." -ForegroundColor Yellow
}