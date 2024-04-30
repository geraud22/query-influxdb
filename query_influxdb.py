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
        "auth_token": request.args.get('auth_token'),
        "org": request.args.get('org'),
        "bucket": request.args.get('bucket'),
        "app_id": request.args.get('app_id'),
        "device_id": request.args.get('device_id'),
        "field": request.args.get('field'),
        "time_range": request.args.get("time_range"),
        "url_port": request.args.get('url_port')
    }
    
    for key,value in parameters.items():
        if value is None:
            return {'error':f'Route expects 9 arguments. Received: {len(parameters)} arguments.'}
    
    url = f"{parameters['url']}:{parameters['url_port']}/api/v2/query?org={parameters['org']}"
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