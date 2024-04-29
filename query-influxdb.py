import requests
from dotenv import load_dotenv
import os

load_dotenv()

INFLUX_URL = os.getenv("INFLUX_URL")
INFLUX_ORG = os.getenv("INFLUX_ORG")
INFLUX_API_TOKEN = os.getenv("INFLUX_API_TOKEN")
INFLUX_QUERY = os.getenv("INFLUX_QUERY")

def query_influxdb():
    url = f"{INFLUX_URL}/api/v2/query?org={INFLUX_ORG}"
    headers = {
        'Content-Type': 'application/vnd.flux',
        'Accept': 'application/csv',
        'Authorization': f'Token {INFLUX_API_TOKEN}'
    }
    data = INFLUX_QUERY

    response = requests.post(url, headers=headers, data=data)
    
    if response.status_code == 200:
        with open('query-data.csv', 'w') as csv_file:
            csv_file.write(response.text)
        return True
    else:
        print(f"Failure Code: {response.status_code}")
        return False
    
if __name__ == "__main__":
    if query_influxdb():
        print(f"CSV data saved to query-data.csv")
    else:
        print("Failed to query InfluxDB")
