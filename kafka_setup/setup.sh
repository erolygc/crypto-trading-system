#!/bin/bash
# Apache Kafka Kurulum Script'i
# Real-time messaging için Kafka cluster

echo "🚀 Kafka Kurulumu Başlatılıyor..."

# Java'yı kontrol et
if ! command -v java &> /dev/null; then
    echo "❌ Java bulunamadı! OpenJDK 8+ gerekli."
    exit 1
fi

echo "📦 Kafka indiriliyor..."
wget -q https://downloads.apache.org/kafka/3.5.0/kafka_2.13-3.5.0.tgz
tar -xzf kafka_2.13-3.5.0.tgz
mv kafka_2.13-3.5.0 kafka

echo "🚀 Kafka servisleri başlatılıyor..."

# Zookeeper'ı başlat
nohup ./kafka/bin/zookeeper-server-start.sh kafka/config/zookeeper.properties > zookeeper.log 2>&1 &
echo "✅ Zookeeper başlatıldı (PID: $!)"
sleep 5

# Kafka'yı başlat  
nohup ./kafka/bin/kafka-server-start.sh kafka/config/server.properties > kafka.log 2>&1 &
echo "✅ Kafka başlatıldı (PID: $!)"
sleep 5

# Test topic oluştur
echo "📋 Test topic oluşturuluyor..."
./kafka/bin/kafka-topics.sh --create --topic crypto-trading --bootstrap-server localhost:9092

echo "✅ Kafka kurulumu tamamlandı!"
echo "🎯 Kafka Broker: localhost:9092"
echo "📊 Kafka UI: http://localhost:8080 (ek kurulum gerekli)"
