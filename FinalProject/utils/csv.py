import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import utils.data_manipulation as dm
from datetime import datetime
def read_weather_data(uploaded_file):
    try:
        if uploaded_file.name.endswith('.csv'):
            return pd.read_csv(uploaded_file)
        elif uploaded_file.name.endswith('.json'):
            return pd.read_json(uploaded_file)
        else:
            raise ValueError("Unsupported file format. Use CSV or JSON.")
    except Exception as e:
        st.error(f"Error reading file: {e}")
        return pd.DataFrame()


def clean_data(data):
    return data.fillna({'temperature': data['temperature'].mean(),
                        'humidity': data['humidity'].mean()})

def save_weather_data_csv(data):
    try:
        data_to_save= dm.rename_data_2_save(data)
        timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
        data_to_save.to_csv(f"weather_data_{timestamp}.csv", index=False)
        st.success("File CSV created OK")
    except IOError as e:
        st.warning("file CSV NOT created, try againg or refresh the current page")

def plot_scatter(data):
    plt.figure(figsize=(8, 6))
    plt.scatter(data['temperature'], data['humidity'], alpha=0.6, c='blue')
    plt.xlabel('Temperature (°C)')
    plt.ylabel('Humidity (%)')
    plt.title('Humidity vs Temperature')
    plt.grid()
    st.pyplot(plt)


def plot_line(data):
    plt.figure(figsize=(10, 6))
    plt.plot(data['date'], data['temperature'], label='Temperature (°C)', marker='o')
    plt.plot(data['date'], data['humidity'], label='Humidity (%)', marker='x')
    plt.xlabel('Date')
    plt.ylabel('Value')
    plt.title('Weather Data Over Time')
    plt.legend()
    plt.grid()
    plt.xticks(rotation=45)
    st.pyplot(plt)