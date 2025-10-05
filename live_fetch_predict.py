import requests
import pandas as pd
import joblib
from datetime import datetime
import os
from send_update import send_update



def fetch_live_weather(api_key, city="Nairobi"):
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
    response = requests.get(url)
    
    if response.status_code != 200:
        print("Error fetching data:", response.status_code, response.text)
        return None
    
    data = response.json()
    
    #extract relevant data
    tavg = data['main']['temp']
    tmin = data['main']['temp_min']
    tmax = data['main']['temp_max']
    wspd = data['wind']['speed'] * 3.6  # Convert m/s to km/
    pres = data['main']['pressure']
    wdir = data['wind'].get('deg', 0)
    prcp = data.get('rain', {}).get('1h', 0)
    wpgt = data['wind'].get('gust', 0) * 3.6  # Convert m/s to km/h
    # Placeholder values for missing features
    
    snow = 0
    tsun = 0
    
    #build feature list
    features = [tavg, tmin, tmax, prcp, snow, wdir, wspd, wpgt, pres, tsun]
    print ("Live weather features:", features)
    return features

# Example usage
api_key = "6fa9eedab5126d0c25891f19af9ae50d"
features = fetch_live_weather(api_key)

if features:
    
    model = joblib.load('rain_prediction_model.pkl')
    
    cols = ['tavg','tmin','tmax',
            'prcp','snow','wdir','wspd',
            'wpgt','pres','tsun']
    live_df = pd.DataFrame([features], columns=cols)
    prediction = model.predict(live_df)[0]
    print(f"\n--- {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} ---\n")
    print(f"Location: Nairobi")
    print(f"Average Temp: {features[0]} °C")
    print(f"Min Temp: {features[1]} °C")
    print(f"Max Temp: {features[2]} °C")
    print(f"Precipitation: {features[3]} mm")   
    print(f"Snow: {features[4]} mm")
    print(f"Wind Direction: {features[5]} °")
    print(f"Wind Speed: {features[6]} km/h")
    print(f"Wind Gust: {features[7]} km/h")
    print(f"Pressure: {features[8]} hPa")
    print(f"Sunshine: {features[9]} min")
    print(f"Rain Prediction: {'Rain' if prediction == 1 else 'No Rain'}")

    prediction_message =(
        f"Weather Update for Nairobi:\n"
        f"Average Temp: {features[0]} °C\n"
        f"Min Temp: {features[1]} °C\n"
        f"Max Temp: {features[2]} °C\n"
        f"Precipitation: {features[3]} mm\n"
        f"Rain Prediction: {'Rain' if prediction == 1 else 'No Rain'}"
    )
    send_update(prediction_message)
                        
    #define log file path
    log_file = 'live_weather_log.csv'
    
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    log_entry = {
        'timestamp': timestamp,
        'tavg': features[0],
        'tmin': features[1],
        'tmax': features[2],
        'prcp': features[3],
        'snow': features[4],
        'wdir': features[5],
        'wspd': features[6],
        'wpgt': features[7],
        'pres': features[8],
        'tsun': features[9],
        'prediction': 'Rain' if prediction == 1 else 'No Rain'
    }

    # Check if log file exists
    df_log = pd.DataFrame([log_entry])
    if not os.path.isfile(log_file):
        df_log.to_csv(log_file, index=False)
    else:
        df_log.to_csv(log_file, mode='a', header=False, index=False)
    print(f"\nLogged data to {log_file}")