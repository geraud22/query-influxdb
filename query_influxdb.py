from flask import Flask, request
from flask_cors import CORS
import requests
from csv2json import csv_to_json, specifyRange

app = Flask(__name__)
CORS(app)

@app.route('/query', methods=['GET'])
def query_influxdb():
    # Define endpoint parameters
    parameters = {
        "host_url": request.args.get('url'),
        "org": request.args.get('org'),
        "auth_token": request.args.get('auth_token'),
        "bucket": request.args.get('bucket'),
        "start_range": request.args.get("start_range"),
        "stop_range": request.args.get('stop_range'),
        "app_id": request.args.get('app_id'),
        "device_id": request.args.get('device_id'),
        "field": request.args.get('field'),
    }
    
    for key, value in parameters.items():
        if value is None or value.strip() == '':
            if key == 'stop_range': # Make the parameter optional.
                continue
            else:
                return {'error': f'Missing argument: {key}'}
    
    url = f"{parameters['host_url']}/api/v2/query?org={parameters['org']}"
    headers = {
        'Content-Type': 'application/vnd.flux',
        'Accept': 'application/csv',
        'Authorization': f'Token {parameters['auth_token']}'
    }
    data = f'''from(bucket: "{parameters['bucket']}")|> {specifyRange(parameters['start_range'], parameters['stop_range'])}
            |> filter(fn: (r) => r["topic"] == "application/{parameters['app_id']}/device/{parameters['device_id']}/event/up")
            |> filter(fn: (r) => r["_field"] == "{parameters['field']}")
            |> yield(name: "last")'''

    response = requests.post(url, headers=headers, data=data)
    
    if response.status_code == 200:
        jsonArray = csv_to_json(response.text)
        return jsonArray
    else:
        return {'error': f'Failed to query InfluxDB. Status code: {response.status_code}. Reason: {response.reason}'}