from kafka import KafkaConsumer
## 도로 Link ID
subway_consumer = KafkaConsumer(
    "subway_position_topic",
    bootstrap_servers="kafka:9092",
    group_id="subway_group",
    auto_offset_reset="earliest",
    enable_auto_commit=True
)

print("🚇 Subway Group Listening...")
for msg in subway_consumer:
    print(f"[{msg.topic}] {msg.value.decode('utf-8')}")
