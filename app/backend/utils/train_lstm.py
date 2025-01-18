#Train LSTM for AQI Forecasting
import numpy as np
import pandas as pd
import tensorflow as tf
from tensorflow import keras
from sklearn.preprocessing import MinMaxScaler
import joblib

# Load dataset
df = pd.read_csv("data/clean/processed_data.csv")

# Feature Scaling
scaler = MinMaxScaler()
df_scaled = scaler.fit_transform(df)

# Create sequences for LSTM
def create_sequences(data, seq_length=10):
    X, y = [], []
    for i in range(len(data) - seq_length):
        X.append(data[i:i + seq_length])
        y.append(data[i + seq_length][1])  # Predict 'pm25' (AQI)
    return np.array(X), np.array(y)

SEQ_LENGTH = 10
X, y = create_sequences(df_scaled, SEQ_LENGTH)

# Train/Test Split
train_size = int(len(X) * 0.8)
X_train, X_test = X[:train_size], X[train_size:]
y_train, y_test = y[:train_size], y[train_size:]

# Build LSTM Model
model = keras.Sequential([
    keras.layers.LSTM(50, return_sequences=True, input_shape=(SEQ_LENGTH, X.shape[2])),
    keras.layers.LSTM(50),
    keras.layers.Dense(1)
])

model.compile(optimizer='adam', loss='mse')

# Train Model
model.fit(X_train, y_train, epochs=20, batch_size=16, validation_data=(X_test, y_test))

# Save model
joblib.dump(model, "models/trained_lstm.pkl")
print("LSTM Model Saved!")
