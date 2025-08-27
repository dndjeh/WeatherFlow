import requests
import pandas as pd
import os
from dotenv import load_dotenv
import xml.etree.ElementTree as ET

load_dotenv()
OUTBREAK_KEY = os.getenv("OUTBREAK_KEY")    #돌발상황
TRAFFIC_INFORMATION = os.getenv('TRAFFIC_INFORMATION')  #교통량
RAIN_API_KEY = os.getenv('RAIN_API_KEY')    #강우량
FLOOD_MAP_API_KEY = os.getenv('FLOOD_MAP_API_KEY')
EARTHQUAKE_SHELTER_API_KEY = os.getenv('EARTHQUAKE_SHELTER_API_KEY')

def get_columns(api_key, service_name, start_index=1, end_index=5, response_type='json'):
    url = f"http://openapi.seoul.go.kr:8088/{api_key}/{response_type}/{service_name}/{start_index}/{end_index}/"
    print("Request URL:", url)
    
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()  # HTTP 에러 체크
        
        if not response.text.strip():
            raise ValueError("빈 응답 발생")

        if response_type.lower() == 'json':
            data = response.json()
            rows = list(data.values())[0].get('row', [])
            df = pd.DataFrame(rows)
            return list(df.columns)
        
        elif response_type.lower() == 'xml':
            root = ET.fromstring(response.text)
            rows = []
            for row in root.findall('row'):
                record = {child.tag: child.text for child in row}
                rows.append(record)
            df = pd.DataFrame(rows)
            return list(df.columns)
        
        else:
            return f"Unsupported response_type: {response_type}"
    
    except requests.exceptions.RequestException as e:
        return f"HTTP Error: {e}"
    except ValueError as ve:
        return f"JSON/Empty Error: {ve}"
    except KeyError as ke:
        return f"Key Error: {ke}"
    except ET.ParseError as pe:
        return f"XML Parse Error: {pe}"

def get_columns_multiple(api_info_list):

    all_columns = {}
    
    for api in api_info_list:
        name = api['name']
        key = api['key']
        response_type = api.get('response_type', 'json')
        cols = get_columns(api_key=key, service_name=name, response_type=response_type)
        all_columns[name] = cols
    
    return all_columns


if __name__ == "__main__":
    api_list = [
        {'name': 'AccInfo', 'key': OUTBREAK_KEY, 'response_type' : 'xml'},
        {'name': 'SpotInfo', 'key': TRAFFIC_INFORMATION, 'response_type':'xml'},
        {'name': 'ListRainfallService', 'key': OUTBREAK_KEY, 'response_type' : 'xml'},
        {'name': 'floodingDs', 'key': FLOOD_MAP_API_KEY, 'response_type' : 'xml'},
        {'name': 'TlEtqkP', 'key': EARTHQUAKE_SHELTER_API_KEY, 'response_type' : 'xml'}
    ]

    columns_dict = get_columns_multiple(api_list)

    for service_name, cols in columns_dict.items():
        print(f"{service_name} 컬럼:")
        print(cols)
        print("="*50)
