import requests
from dotenv import load_dotenv
import os
from csv2json import csv_to_json
from flux_query_creator import createFluxQuery

load_dotenv()

INFLUX_URL = os.getenv("INFLUX_URL")
INFLUX_ORG = os.getenv("INFLUX_ORG")
INFLUX_API_TOKEN = os.getenv("INFLUX_API_TOKEN")

def query_influxdb():
    url = f"{INFLUX_URL}/api/v2/query?org={INFLUX_ORG}"
    headers = {
        'Content-Type': 'application/vnd.flux',
        'Accept': 'application/csv',
        'Authorization': f'Token {INFLUX_API_TOKEN}'
    }
    data = createFluxQuery()

    response = requests.post(url, headers=headers, data=data)
    
    if response.status_code == 200:
        csv_to_json(response.text, 'query-data.json')
        return True
    else:
        print(f"Failure Code: {response.status_code} : {response.text}")
        return False
    
if __name__ == "__main__":
    if query_influxdb():
        print(f"CSV data saved to query-data.json")
