from kafka import KafkaConsumer
import json
import time

# Kafka Consumer 생성 (재시도 로직 추가)
while True:
    try:
        consumer = KafkaConsumer(
            'weather-topic',                # 구독할 토픽
            bootstrap_servers='kafka:9092', # Docker 네트워크에서 Kafka 서비스 이름
            value_deserializer=lambda v: json.loads(v.decode('utf-8')), # JSON → dict
            auto_offset_reset='latest',   # auto_offset_reset은 Consumer가 그룹에 offset 기록이 없거나 초기화되었을 때 동작을 결정
            enable_auto_commit=True,        # 자동 커밋
            group_id='DB_group'             # 컨슈머 그룹 ID
        )
        print("📡 Kafka Consumer 시작. 날씨 데이터 수신 대기 중...", flush=True)
        break  # 성공하면 루프 종료
    except Exception as e:
        print("Kafka 연결 실패, 5초 후 재시도:", e, flush=True)
        time.sleep(5)  # 5초 후 재시도

# 메시지 수신
for message in consumer:
    data = message.value
    print(f"📥 수신한 데이터: {data}", flush=True)
