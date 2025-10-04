# app.py - Versión Final Corregida y Segura

from flask import Flask, request, jsonify
from flask_cors import CORS
import joblib
import pandas as pd
import requests
from datetime import datetime
from dateutil.relativedelta import relativedelta
import os # Importante para leer variables de entorno

# --- CONFIGURACIÓN ---
app = Flask(__name__)
CORS(app)

# --- SEGURIDAD: OBTENER API KEY DESDE EL ENTORNO DE RENDER ---
# La clave secreta se configura en la web de Render, no aquí.
OPENWEATHERMAP_API_KEY = os.environ.get('OPENWEATHERMAP_API_KEY')

# --- ORDEN EXACTO DE CARACTERÍSTICAS QUE EL MODELO APRENDIÓ ---
# Esta lista garantiza que los datos se presenten al modelo en el orden correcto.
FEATURE_ORDER = [
    'T2M_lag_1', 'RH2M_lag_1', 'WS2M_lag_1', 'PS_lag_1',
    'T2M_lag_2', 'RH2M_lag_2', 'WS2M_lag_2', 'PS_lag_2',
    'T2M_lag_3', 'RH2M_lag_3', 'WS2M_lag_3', 'PS_lag_3',
    'T2M_lag_4', 'RH2M_lag_4', 'WS2M_lag_4', 'PS_lag_4',
    'T2M_lag_5', 'RH2M_lag_5', 'WS2M_lag_5', 'PS_lag_5',
    'T2M_lag_6', 'RH2M_lag_6', 'WS2M_lag_6', 'PS_lag_6',
    'month'
]

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
    if not OPENWEATHERMAP_API_KEY:
        print("Error: La clave de API de OpenWeatherMap no está configurada en el entorno.")
        return None
    try:
        url = f"https://api.openweathermap.org/data/3.0/onecall?lat={lat}&lon={lng}&exclude=current,minutely,hourly,alerts&appid={OPENWEATHERMAP_API_KEY}&units=metric&lang=es"
        response = requests.get(url, timeout=10)
        data = response.json()
        if response.status_code == 200:
            forecast_list = []
            for dia in data['daily'][:5]:
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
        response = requests.get(base_url, params=params, timeout=20)
        nasa_data = response.json()
        
        df = pd.DataFrame(nasa_data['properties']['parameter'])
        df.index = pd.to_datetime(df.index, format='%Y%m%d%H')
        df.replace(-999, pd.NA, inplace=True)
        monthly_avg = df.resample('M').mean()
        last_6_months = monthly_avg.iloc[-7:-1]
        
        features = {}
        # Iteramos de forma inversa de una manera más robusta
        for i in range(len(last_6_months)):
            row = last_6_months.iloc[len(last_6_months) - 1 - i]
            lag = i + 1
            features[f'T2M_lag_{lag}'] = row['T2M']
            features[f'RH2M_lag_{lag}'] = row['RH2M']
            features[f'WS2M_lag_{lag}'] = row['WS2M']
            features[f'PS_lag_{lag}'] = row['PS']
        
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

    daily_forecast = get_daily_forecast(float(lat), float(lng))
    features_for_ml = get_features_from_nasa(float(lat), float(lng))
    
    ml_prediction = None
    if features_for_ml and MODELS:
        try:
            input_df_unordered = pd.DataFrame(features_for_ml, index=[0])
            # Forzar el DataFrame a tener el orden exacto de columnas que el modelo espera.
            input_df_ordered = input_df_unordered[FEATURE_ORDER]

            predictions = {}
            for var, model in MODELS.items():
                pred = model.predict(input_df_ordered)
                predictions[var] = round(float(pred[0]), 2)
            ml_prediction = {
                "temperature_celsius": predictions.get('T2M'),
                "humidity_percent": predictions.get('RH2M'),
                "wind_speed_ms": predictions.get('WS2M'),
                "pressure_kpa": predictions.get('PS')
            }
        except Exception as e:
            print(f"Error en predicción de IA: {e}")
            ml_prediction = {"error": "No se pudo generar la predicción del modelo."}

    final_response = {
        "location": f"Lima, Peru (lat: {lat}, lon: {lng})",
        "short_term_forecast_5_days": daily_forecast,
        "long_term_ml_prediction_next_month_avg": ml_prediction
    }
    
    return jsonify(final_response)