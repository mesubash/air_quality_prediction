from flask import Flask, request, jsonify
from flask_cors import CORS
import joblib
import numpy as np
import requests 
from utils.data_fetcher import fetch_live_data
from utils.forecast import forecast_aqi

app = Flask(__name__)
CORS(app)


    
    
# Load trained models
rf_model = joblib.load('models/trained_rf.pkl')

@app.route('/predict', methods=['POST'])
def predict():
    data = request.json
    features = np.array([data['PM2.5'], data['PM10'], data['NO2'], data['CO'], data['temperature'], data['humidity']]).reshape(1, -1)
    prediction = rf_model.predict(features)
    return jsonify({'AQI': prediction[0]})

@app.route('/live_aqi', methods=['GET'])
def live_aqi():
    data = fetch_live_data()
    return jsonify(data)

@app.route('/forecast', methods=['GET'])
def forecast():
    forecasted_values = forecast_aqi()
    return jsonify(forecasted_values)

if __name__ == '__main__':
    app.run(debug=True)
