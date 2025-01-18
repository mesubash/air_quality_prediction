# Data cleaning
import pandas as pd
import numpy as np 
import glob
from sklearn.preprocessing import MinMaxScaler


def clean_merge():
    # Step 1: Find all CSV files recursively inside folders
    csv_files_air = glob.glob("data/raw/air/openaq/data20*/**/*.csv", recursive=True)
    csv_files_weather = glob.glob("data/raw/weather/open-meteo/open-meteo-202*.csv", recursive=True)

    # Step 2: Load all CSVs and store them in a list
    df_list1 = []
    for file in csv_files_air:  
        df = pd.read_csv(file) 
        df_list1.append(df)     
        
    df_list2 = []
    for file in csv_files_weather:
        df = pd.read_csv(file, skiprows=2)  # Skip the first two rows
        df.reset_index(drop=True, inplace=True) 
        df_list2.append(df)  # Append to list
        
    # Step 3: Concatenate all dataframes into one
    merged_df1 = pd.concat(df_list1, ignore_index=True)
    merged_df2 = pd.concat(df_list2, ignore_index=True)


    # Step 4: Ensure date column is correctly formatted (adjust the column name if needed)
    date_column_a = "datetime"  # Change this if your date column has a different name
    merged_df1[date_column_a] = pd.to_datetime(merged_df1[date_column_a], errors='coerce')

    date_column_w = "time"  # Change this if your date column has a different name
    merged_df2[date_column_w] = pd.to_datetime(merged_df2[date_column_w], errors='coerce')


    #sorting the data according to date
    merged_df1 = merged_df1.sort_values(by=date_column_a)
    merged_df2 = merged_df2.sort_values(by=date_column_w)


    #saving files as csv
    merged_df1.to_csv("data/clean/air_sorted_merged_data.csv", index=False)
    merged_df2.to_csv("data/clean/weather_sorted_merged_data.csv", index=False)


    print("✅ Merging & sorting completed Air Data!")

# Combine data
def merge_data():
    # Load datasets and fetch API data
    df_air = pd.read_csv("data/clean/air_sorted_merged_data.csv")
    df_weather = pd.read_csv("data/clean/weather_sorted_merged_data.csv")

    # Pivot the data to have 'pm25' and 'o3' in separate columns
    df_air = df_air.pivot(index='datetime', columns='parameter', values='value').reset_index()

    # Convert 'datetime' to proper datetime format and remove timezone
    df_air['datetime'] = pd.to_datetime(df_air['datetime']).dt.tz_localize(None)

    # Format as 'YYYY-MM-DD HH:MM:SS'
    df_air['datetime'] = df_air['datetime'].dt.strftime('%Y-%m-%d %H:%M:%S')

    # Delete the first row from df_weather
    df_weather = df_weather.iloc[1:].reset_index(drop=True)  

    # Rename 'time' to 'datetime' in df_weather
    df_weather = df_weather.rename(columns={'time': 'datetime'})

    # Convert 'datetime' to the same format in both dataframes
    df_weather['datetime'] = pd.to_datetime(df_weather['datetime']).dt.strftime('%Y-%m-%d %H:%M:%S')

    # Merge both datasets based on 'datetime' column
    merged_df = pd.merge(df_weather, df_air, on='datetime', how='left')

    # Extract newly added columns (from df_air)
    new_columns = [col for col in df_air.columns if col != 'datetime']

    # Define the correct column order
    ordered_cols = ['datetime'] + new_columns + [col for col in merged_df.columns if col not in ['datetime'] + new_columns]

    # Reorder dataframe
    merged_df = merged_df[ordered_cols]

    merged_df.rename(columns={
    
        'o3': 'O3',
        'pm25': 'PM2.5',
        'temperature_2m (°C)': 'Temperature',
        'relative_humidity_2m (%)': 'Humidity',
        'dew_point_2m (°C)': 'Dew_Point',
        'precipitation (mm)': 'Precipitation',
        'pressure_msl (hPa)': 'Pressure_MSL',
        'wind_speed_10m (km/h)': 'Wind_Speed',
        'wind_direction_10m (°)': 'Wind_Direction'
        
        
    }, inplace=True)


    merged_df.head()
    # dataset = pd.concat([df_air,])
    return merged_df



def preprocess_data(file_path):
    # Load merged dataset
    df = pd.read_csv(file_path)

   # Select relevant columns for AQI prediction
    df = df[['O3', 'PM2.5', 'Temperature', 'Humidity',
             'Dew_Point', 'Precipitation', 'Pressure_MSL',
             'Wind_Speed', 'Wind_Direction']]

       # Handle missing values using forward fill
    df.ffill(inplace=True)

    # Normalize numerical features
    scaler = MinMaxScaler()
    df[df.columns] = scaler.fit_transform(df)

    # Save processed data
    df.to_csv("data/clean/processed_data.csv", index=False)
    print("Data Preprocessing Complete!")
    
    return df


if __name__ == "__main__":
    clean_merge()
    df = merge_data()
    if df is not None:
        print(df.head())
        # Save the merged dataset 
        df.to_csv("data/clean/final_merged_clean_dataset.csv", index=False)
        preprocess_data("data/clean/final_merged_clean_dataset.csv")
    else:
        print("Error")