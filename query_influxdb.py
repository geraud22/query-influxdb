from flask import Flask
import requests
from dotenv import load_dotenv
import os
from csv2json import csv_to_json
from flux_query_creator import createFluxQuery

load_dotenv()

INFLUX_URL = os.getenv("INFLUX_URL")
INFLUX_ORG = os.getenv("INFLUX_ORG")
INFLUX_API_TOKEN = os.getenv("INFLUX_API_TOKEN")


app = Flask(__name__)

@app.route('/query', methods=['GET'])
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
        jsonArray = csv_to_json(response.text, 'query-data.json')
        return jsonArray
    else:
        return {'error': f'Failed to query InfluxDB. Status code: {response.status_code}. Reason: {response.reason}'}
    
if __name__ == "__main__":
    app.run(debug=True, port=5000)
