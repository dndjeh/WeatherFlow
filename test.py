import time
from kafka import KafkaProducer, KafkaConsumer
from kafka.errors import NoBrokersAvailable

# Kafka Producer 연결 시도 (재시도 로직)
while True:
    try:
        producer = KafkaProducer(
            bootstrap_servers='kafka:9092',
            max_request_size=1500000000
        )
        print("Kafka broker connected!")
        break
    except NoBrokersAvailable:
        print("Kafka broker not available, retrying in 5 seconds...")
    except Exception as e:
        print(f"Unexpected error: {e}")
    time.sleep(5)

# Kafka Consumer 생성 및 메시지 읽기
consumer = KafkaConsumer(
    'your_topic_name',
    bootstrap_servers='kafka:9092',
    auto_offset_reset='earliest',
    enable_auto_commit=True,
    group_id='your_group_id',
    consumer_timeout_ms=1000,
    max_partition_fetch_bytes=1500000000,
    fetch_max_bytes=1500000000
)

try:
    for message in consumer:
        print(f"Received message: {message.value}")
finally:
    consumer.close()
