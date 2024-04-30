from flask import Flask, request
from flask_cors import CORS
import requests
from csv2json import csv_to_json

app = Flask(__name__)
CORS(app)

@app.route('/query', methods=['GET'])
def query_influxdb():
    # Define endpoint parameters
    parameters = {
        "url": request.args.get('url'),    
        "organisation": request.args.get('organisation'),
        "auth_token": request.args.get('token'),
        "bucket": request.args.get('bucket'),
        "app_id": request.args.get('app-id'),
        "device_id": request.args.get('device-id'),
        "field": request.args.get('field'),
        "time_range": request.args.get("time-range"),
    }
    
    for key,value in parameters.items():
        if value is None:
            return {'error': 'Route received insufficient arguments.'}
    
    url = f"{parameters['url']}/api/v2/query?org={parameters['organisation']}"
    headers = {
        'Content-Type': 'application/vnd.flux',
        'Accept': 'application/csv',
        'Authorization': f'Token {parameters['auth_token']}'
    }
    data = f'''from(bucket: "{parameters['bucket']}")|> range(start: {parameters['time_range']})
            |> filter(fn: (r) => r["topic"] == "application/{parameters['app_id']}/device/{parameters['device_id']}/event/up")
            |> filter(fn: (r) => r["_field"] == "{parameters['field']}")
            |> yield(name: "last")'''

    response = requests.post(url, headers=headers, data=data)
    
    if response.status_code == 200:
        jsonArray = csv_to_json(response.text)
        return jsonArray
    else:
        return {'error': f'Failed to query InfluxDB. Status code: {response.status_code}. Reason: {response.reason}'}
