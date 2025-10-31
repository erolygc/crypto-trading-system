#!/bin/bash
# TimescaleDB Kurulum Script'i
# PostgreSQL + TimescaleDB Extension

echo "🗄️ Veritabanı Kurulumu Başlatılıyor..."

# Docker'ı kontrol et
if ! command -v docker &> /dev/null; then
    echo "❌ Docker bulunamadı!"
    exit 1
fi

echo "📦 TimescaleDB Docker imajı indiriliyor..."
docker pull timescale/timescaledb:latest-pg14

echo "🚀 Veritabanı container'ı başlatılıyor..."
docker run -d \
    --name crypto-timescaledb \
    -e POSTGRES_PASSWORD=secure_password \
    -e POSTGRES_DB=crypto_trading \
    -p 5432:5432 \
    timescale/timescaledb:latest-pg14

echo "⏳ Veritabanı başlatılması bekleniyor..."
sleep 10

echo "🔧 TimescaleDB extension'ı etkinleştiriliyor..."
docker exec -i crypto-timescaledb psql -U postgres -d crypto_trading << EOF
CREATE EXTENSION IF NOT EXISTS timescaledb CASCADE;
SELECT version();
EOF

echo "📋 Hyper table oluşturuluyor..."
docker exec -i crypto-timescaledb psql -U postgres -d crypto_trading << EOF
CREATE TABLE crypto_klines (
    time TIMESTAMPTZ NOT NULL,
    symbol VARCHAR(20) NOT NULL,
    timeframe VARCHAR(10) NOT NULL,
    open_price DECIMAL(20,8) NOT NULL,
    high_price DECIMAL(20,8) NOT NULL,
    low_price DECIMAL(20,8) NOT NULL,
    close_price DECIMAL(20,8) NOT NULL,
    volume DECIMAL(20,8) NOT NULL
);

SELECT create_hypertable('crypto_klines', 'time');
CREATE INDEX ON crypto_klines (symbol, timeframe, time DESC);
EOF

echo "✅ TimescaleDB kurulumu tamamlandı!"
echo "🔗 Bağlantı: postgresql://postgres:secure_password@localhost:5432/crypto_trading"
