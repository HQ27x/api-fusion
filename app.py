# app.py - API Híbrida de Predicción del Clima

from flask import Flask, request, jsonify
from flask_cors import CORS
import joblib
import pandas as pd
import requests
from datetime import datetime
from dateutil.relativedelta import relativedelta

# --- CONFIGURACIÓN ---
app = Flask(__name__)
CORS(app)

# ¡¡MUY IMPORTANTE!! Pega tus claves de API aquí
OPENWEATHERMAP_API_KEY = "b9887004fb83b6baf80ea22a539cc923"

# --- CARGA DE TUS MODELOS DE IA ---
MODELS = {}
TARGET_VARIABLES = ['T2M', 'RH2M', 'WS2M', 'PS']
print("Cargando modelos de IA locales...")
for var in TARGET_VARIABLES:
    try:
        filename = f'model_{var}.joblib'
        MODELS[var] = joblib.load(filename)
        print(f"✅ Modelo '{filename}' cargado.")
    except Exception as e:
        print(f"❌ Error al cargar '{filename}': {e}")

# --- FUNCIÓN 1: OBTENER PRONÓSTICO DIARIO (OpenWeatherMap) ---
def get_daily_forecast(lat, lng):
    print("🌦️  Obteniendo pronóstico diario de OpenWeatherMap...")
    try:
        url = f"https://api.openweathermap.org/data/3.0/onecall?lat={lat}&lon={lng}&exclude=current,minutely,hourly,alerts&appid={OPENWEATHERMAP_API_KEY}&units=metric&lang=es"
        response = requests.get(url)
        data = response.json()
        if response.status_code == 200:
            forecast_list = []
            for dia in data['daily'][:5]: # Tomamos los próximos 5 días
                fecha = datetime.fromtimestamp(dia['dt'])
                forecast_list.append({
                    "date": fecha.strftime('%Y-%m-%d'),
                    "day_name": fecha.strftime('%A'),
                    "temp_min_celsius": dia['temp']['min'],
                    "temp_max_celsius": dia['temp']['max'],
                    "condition": dia['weather'][0]['description'].capitalize()
                })
            return forecast_list
    except Exception as e:
        print(f"Error en OpenWeatherMap: {e}")
    return None

# --- FUNCIÓN 2: OBTENER Y PROCESAR DATOS HISTÓRICOS (NASA) ---
def get_features_from_nasa(lat, lng):
    print("🛰️  Obteniendo datos históricos de NASA POWER...")
    try:
        base_url = "https://power.larc.nasa.gov/api/temporal/hourly/point"
        end_date = datetime.now() - relativedelta(days=5)
        start_date = end_date - relativedelta(months=7)
        params = {"start": start_date.strftime("%Y%m%d"), "end": end_date.strftime("%Y%m%d"), "latitude": lat, "longitude": lng, "community": "re", "parameters": "T2M,RH2M,WS2M,PS", "format": "json"}
        response = requests.get(base_url, params=params)
        nasa_data = response.json()
        
        # Procesar los datos
        df = pd.DataFrame(nasa_data['properties']['parameter'])
        df.index = pd.to_datetime(df.index, format='%Y%m%d%H')
        df.replace(-999, pd.NA, inplace=True)
        monthly_avg = df.resample('M').mean()
        last_6_months = monthly_avg.iloc[-7:-1]
        
        features = {}
        for i, row in enumerate(reversed(last_6_months.itertuples())):
            lag = i + 1
            features[f'T2M_lag_{lag}'] = row.T2M
            features[f'RH2M_lag_{lag}'] = row.RH2M
            features[f'WS2M_lag_{lag}'] = row.WS2M
            features[f'PS_lag_{lag}'] = row.PS
        features['month'] = datetime.now().month
        return features
    except Exception as e:
        print(f"Error procesando datos de NASA: {e}")
    return None

# --- RUTA PRINCIPAL DE LA API ---
@app.route('/predict/full', methods=['GET'])
def predict_full():
    lat = request.args.get('lat')
    lng = request.args.get('lng')
    if not lat or not lng:
        return jsonify({'error': 'Parámetros "lat" y "lng" son requeridos.'}), 400

    # 1. Obtener pronóstico a corto plazo
    daily_forecast = get_daily_forecast(float(lat), float(lng))

    # 2. Obtener y procesar datos para el modelo de IA
    features_for_ml = get_features_from_nasa(float(lat), float(lng))
    
    ml_prediction = None
    if features_for_ml and MODELS:
        try:
            input_df = pd.DataFrame(features_for_ml, index=[0])
            predictions = {}
            for var, model in MODELS.items():
                pred = model.predict(input_df)
                predictions[var] = round(float(pred[0]), 2)
            ml_prediction = {
                "temperature_celsius": predictions.get('T2M'),
                "humidity_percent": predictions.get('RH2M'),
                "wind_speed_ms": predictions.get('WS2M'),
                "pressure_kpa": predictions.get('PS')
            }
        except Exception as e:
            print(f"Error en predicción de IA: {e}")

    # 3. Construir la respuesta final
    final_response = {
        "location": f"Lima, Peru (lat: {lat}, lon: {lng})",
        "short_term_forecast_5_days": daily_forecast,
        "long_term_ml_prediction_next_month_avg": ml_prediction
    }
    
    return jsonify(final_response)