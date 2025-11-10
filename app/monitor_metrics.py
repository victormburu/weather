from flask import Flask
import requests
from prometheus_client import Gauge, generate_latest, CONTENT_TYPE_LATEST

app = Flask(__name__)
temperature_gauge = Gauge('weather_temperature_celsius', 'Current temperature in Celsius')
rain_prediction = Gauge('weather_precipitation_mm', 'Current precipitation in mm')

@app.route('/metrics')
def metrics():
    return generate_latest(), 200, {'Content-Type': CONTENT_TYPE_LATEST}

def update_metrics(temperature, rain):
    temperature_gauge.set(temperature)
    rain_prediction.set(1 if rain == "Yes Rain" else 0)
    
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)