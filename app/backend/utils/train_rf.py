import pandas as pd
import joblib
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, mean_squared_error

# Load preprocessed dataset
df = pd.read_csv("data/clean/processed_data.csv")

# Features & target (assuming 'pm25' is the AQI proxy)
X = df[['O3', 'Temperature', 'Humidity',
        'Dew_Point', 'Precipitation', 'Pressure_MSL',
        'Wind_Speed', 'Wind_Direction']]
y = df['PM2.5']  # Predicting AQI based on PM2.5

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train Random Forest model
rf_model = RandomForestRegressor(n_estimators=100, random_state=42)
rf_model.fit(X_train, y_train)

# Evaluate model
y_pred = rf_model.predict(X_test)
print("MAE:", mean_absolute_error(y_test, y_pred))
print("MSE:", mean_squared_error(y_test, y_pred))

# Save trained model
joblib.dump(rf_model, "models/trained_rf.pkl")
print("Random Forest Model saved!")
