# Data cleaning
import pandas as pd
import numpy as np 
import glob

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

