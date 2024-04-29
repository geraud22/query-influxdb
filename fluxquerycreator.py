from dotenv import load_dotenv
import os
load_dotenv()

INFLUX_QUERY_BUCKET = os.getenv("INFLUX_QUERY_BUCKET")
INFLUX_QUERY_APP_ID = os.getenv("INFLUX_QUERY_APP_ID")
INFLUX_QUERY_DEVICE_ID = os.getenv("INFLUX_QUERY_DEVICE_ID")
INFLUX_QUERY_FIELD = os.getenv("INFLUX_QUERY_FIELD")

def createFluxQuery():
    return f'''from(bucket: "{INFLUX_QUERY_BUCKET}")|> range(start: -3h)
            |> filter(fn: (r) => r["topic"] == "application/{INFLUX_QUERY_APP_ID}/device/{INFLUX_QUERY_DEVICE_ID}/event/up")
            |> filter(fn: (r) => r["_field"] == "{INFLUX_QUERY_FIELD}")
            |> yield(name: "last")'''