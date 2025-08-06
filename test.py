from kafka import KafkaProducer
import requests
import json
import time

API_KEY = "YOUR_API_KEY"
CITIES = ["Seoul", "New York", "Tokyo", "Paris", "Sydney"]

producer = KafkaProducer(
    bootstrap_servers='localhost:9092',
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

while True:
    for city in CITIES:
        url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
        res = requests.get(url)
        data = res.json()

        # 필요한 필드만 추출
        filtered = {
            "city": city,
            "temp": data["main"]["temp"],
            "humidity": data["main"]["humidity"],
            "weather": data["weather"][0]["main"],
            "timestamp": data["dt"]
        }

        producer.send("weather-topic", filtered)
        print(f"✅ {city} 데이터 전송됨:", filtered)

    time.sleep(60)  # 1분 간격으로 수집
