#!/bin/bash
# Dashboard Kurulum Script'i
# Grafana + InfluxDB + Prometheus + Crypto Collector

echo "📊 Dashboard Kurulumu Başlatılıyor..."

# Docker'ı kontrol et
if ! command -v docker &> /dev/null; then
    echo "❌ Docker bulunamadı! Önce Docker'ı kurun."
    exit 1
fi

if ! command -v docker-compose &> /dev/null; then
    echo "❌ Docker Compose bulunamadı!"
    exit 1
fi

echo "✅ Docker hazır!"

# .env dosyasını kontrol et
if [ ! -f ".env" ]; then
    echo "⚠️ .env dosyası bulunamadı. .env.example'dan kopyalanıyor..."
    cp .env.example .env
    echo "📝 Lütfen .env dosyasını düzenleyin."
fi

# Servisleri başlat
echo "🚀 Servisler başlatılıyor..."
docker-compose up -d

echo "✅ Dashboard kurulumu tamamlandı!"
echo "🌐 Grafana: http://localhost:3000 (admin/admin123)"
echo "📈 InfluxDB: http://localhost:8086"
echo "🎯 Prometheus: http://localhost:9090"
