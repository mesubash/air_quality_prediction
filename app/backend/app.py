from flask import Flask, request, jsonify
from flask_cors import CORS
import joblib
import numpy as np
import requests 
from utils.data_fetcher import fetch_live_data
from flask_cors import CORS
# from utils.forecast import forecast_aqi

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "http://localhost:5173"}})


    
# Load trained models
rf_model = joblib.load('models/trained_rf.pkl')
lstm_model = joblib.load('models/trained_lstm.pkl')

@app.route('/predict', methods=['POST'])
def predict():
   data = request.json
   features = np.array([data['O3'], data['Temperature'], data['Humidity'],
                         data['Dew_Point'], data['Precipitation'], data['Pressure_MSL'],
                         data['Wind_Speed'], data['Wind_Direction']]).reshape(1, -1)
   prediction = rf_model.predict(features)
   return jsonify({'AQI': prediction[0]})

@app.route('/live_aqi', methods=['GET'])
def live_aqi():
    data = fetch_live_data()
    return jsonify(data)

@app.route('/forecast', methods=['GET'])
def forecast():
    dummy_input = np.random.rand(1, 10, 8)  # Adjust shape based on your LSTM input
    future_forecast = lstm_model.predict(dummy_input)
    return jsonify({'forecast': future_forecast.tolist()})


if __name__ == '__main__':
    app.run(debug=True)
