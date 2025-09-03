import time
import os
import json
import requests
import xml.etree.ElementTree as ET
from kafka import KafkaProducer
from dotenv import load_dotenv


load_dotenv()
OUTBREAK_KEY = os.getenv("OUTBREAK_KEY")    # 돌발정보
TRAFFIC_INFORMATION = os.getenv("TRAFFIC_INFORMATION") # 교통량
RAIN_API_KEY = os.getenv("RAIN_API_KEY")    # 강우량


### 지하철 현재 위치는 모든 호선을 가져 와야하고, 도착 정보는 다 가져올지 아니면 웹에서 요청한 것만 가져올지,
SEOUL_SUBWAY_ARRIVAL_API_KEY = os.getenv("SEOUL_SUBWAY_ARRIVAL_API_KEY") # 역명 필요 http://swopenAPI.seoul.go.kr/api/subway/(인증키)/xml/realtimeStationArrival/(시작 페이지)/(종료페이지)/(역명)
SEOUL_SUBWAY_POSITION_API_KEY = os.getenv("SEOUL_SUBWAY_POSITION_API_KEY") # 지하철 호선 필요 http://swopenAPI.seoul.go.kr/api/subway/(인증키)/xml/realtimePosition/(시작 페이지)/(종료페이지)/(호선) -> ex) 1호선

### 링크 아이디 필요
SEOUL_TRAFFIC_REALTIME_API_KEY = os.getenv("SEOUL_TRAFFIC_REALTIME_API_KEY") # 링크 아이디 필요 http://openapi.seoul.go.kr:8088/(인증키)/xml/TrafficInfo/(시작 페이지)/(종료페이지)/(링크 아이디) -> ex) 1220003800

#SEOUL_TRANSIT_API_KEY = os.getenv("SEOUL_TRANSIT_API_KEY")  # 환승 정보

if __name__ == "__main__":
    api_list = [
        {'name': 'AccInfo', 'key': OUTBREAK_KEY, 'response_type' : 'xml'},
        {'name': 'SpotInfo', 'key': TRAFFIC_INFORMATION, 'response_type':'xml'},
        {'name': 'ListRainfallService', 'key': RAIN_API_KEY, 'response_type' : 'xml'},

        {'name': 'realtimeStationArrival', 'key': SEOUL_SUBWAY_ARRIVAL_API_KEY, 'response_type' : 'xml'},
        {'name': 'realtimePosition', 'key': SEOUL_SUBWAY_POSITION_API_KEY, 'response_type' : 'xml'},
        {'name': 'TrafficInfo', 'key': SEOUL_TRAFFIC_REALTIME_API_KEY, 'response_type' : 'xml'}
    ]


# -----------------------------
# 토픽 매핑
# -----------------------------
topic_mapping = {
    'AccInfo': 'outbreak_topic',
    'SpotInfo': 'traffic_topic',
    'ListRainfallService': 'rain_topic',
    'realtimeStationArrival': 'subway_arrival_topic',
    'realtimePosition': 'subway_position_topic',
    'TrafficInfoRealtime': 'realtime_traffic_topic',
    'TrafficInfo': 'realtime_trafficInfo'
}

# -----------------------------
# XML → dict 변환 함수
# -----------------------------
def parse_xml_to_dict(xml_str):
    root = ET.fromstring(xml_str)
    result = []
    for row in root.findall('.//row'):
        row_dict = {}
        for elem in row:
            row_dict[elem.tag] = elem.text
        result.append(row_dict)
    return result

# -----------------------------
# Kafka 연결
# -----------------------------
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

# -----------------------------
# 데이터 전송 함수
# -----------------------------
def send_to_kafka(api):
    api_name = api['name']
    response_type = api['response_type']
    topic = topic_mapping[api_name]

    # 실제 공공데이터 API URL 예시
    url = f"http://openapi.seoul.go.kr:8088/{api['key']}/{response_type}/{api_name}/{1}/{4}/"
    
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        if api['response_type'] == 'xml':
            data_dict = parse_xml_to_dict(response.text)
        else:
            data_dict = response.json()
        
        producer.send(topic, data_dict)
        producer.flush()
        print(f"{api_name} 데이터 → 토픽 '{topic}' 전송 완료!", flush=True)
        print("전송 데이터 샘플:", data_dict, flush=True)

    except Exception as e:
        print(f"{api_name} 데이터 전송 실패:", e, flush=True)

# -----------------------------
# 주기적 실행
# -----------------------------
while True:
    for api in api_list:
        send_to_kafka(api)
    time.sleep(5)  # 5초 주기
