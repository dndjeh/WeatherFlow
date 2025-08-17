import time
from kafka import KafkaProducer
import json
import os
import requests

API_KEY = os.getenv("API_KEY")

CITIES = ["Seoul", "New York", "Tokyo", "Paris", "Sydney"]

while True:
    try:
        print("Kafka 연결 시도 중...", flush=True)
        producer = KafkaProducer(
            bootstrap_servers='kafka:9092',
            value_serializer=lambda v: json.dumps(v).encode('utf-8')
        )
        print("Kafka 연결 성공!", flush=True)
        break
    except Exception as e:
        print("Kafka 연결 실패, 5초 후 재시도:", e, flush=True)
        time.sleep(5)

while True:
    for city in CITIES:
        
        url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
        res = requests.get(url)
        data = res.json()
        filtered = {
            "city": city,
            "temp": data["main"]["temp"],
            "humidity": data["main"]["humidity"],
            "weather": data["weather"][0]["main"],
            "timestamp": data["dt"]
        }
        producer.send("weather-topic", filtered)
        print(f"✅ {city} 데이터 전송됨:", filtered, flush=True)
        time.sleep(10)
