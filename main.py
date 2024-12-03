import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st
import requests
from datetime import datetime, timedelta

# Función para leer datos
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

# Función para limpiar datos
def clean_data(data):
    return data.fillna({'temperature': data['temperature'].mean(),
                        'humidity': data['humidity'].mean()})

# Función para graficar dispersión
def plot_scatter(data):
    plt.figure(figsize=(8, 6))
    plt.scatter(data['temperature'], data['humidity'], alpha=0.6, c='blue')
    plt.xlabel('Temperature (°C)')
    plt.ylabel('Humidity (%)')
    plt.title('Humidity vs Temperature')
    plt.grid()
    st.pyplot(plt)

# Función para graficar líneas
def plot_line(data):
    plt.figure(figsize=(10, 6))
    plt.plot(data['date'], data['temperature'], label='Temperature (°C)', marker='o')
    plt.plot(data['date'], data['humidity'], label='Humidity (%)', marker='x')
    plt.xlabel('Date')
    plt.ylabel('Value')
    plt.title('Weather Data Over Time')
    plt.legend()
    plt.grid()
    st.pyplot(plt)

# Obtener datos desde una API
def fetch_weather_data(api_key, city):
    #https://openweathermap.org/history
    #577206faeeaec391fc2a40775b0830da       key
    #577206faeeaec391fc2a40775b0830da
    #url = f"http://api.openweathermap.org/data/2.5/weather?q=bogota,col&appid=577206faeeaec391fc2a40775b0830da&units=metric"
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error: {response.status_code}")
        return None

# Función para obtener datos históricos de Open-Meteo
def fetch_open_meteo_data(latitude, longitude, start_date, end_date):
    url = "https://archive-api.open-meteo.com/v1/archive"
    params = {
        "latitude": latitude,
        "longitude": longitude,
        "start_date": start_date.strftime("%Y-%m-%d"),
        "end_date": end_date.strftime("%Y-%m-%d"),
        "hourly": "temperature_2m,relative_humidity_2m",
        "timezone": "auto"
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error: {response.status_code}")
        return None

# Procesar datos en un DataFrame
def process_open_meteo_data(data):
    hourly_data = data.get("hourly", {})
    dates = hourly_data.get("time", [])
    temperatures = hourly_data.get("temperature_2m", [])
    humidities = hourly_data.get("relative_humidity_2m", [])

    records = []
    for date, temp, hum in zip(dates, temperatures, humidities):
        records.append({"date": date, "temperature": temp, "humidity": hum})
    return pd.DataFrame(records)

# Visualizar los datos
def plot_weather_data(df):
    plt.figure(figsize=(12, 6))

    # Graficar temperatura
    plt.plot(df['date'], df['temperature'], label="Temperature (°C)", color='orange', marker='o')

    # Graficar humedad
    plt.plot(df['date'], df['humidity'], label="Humidity (%)", color='blue', marker='x')

    plt.title("Historical Weather Data from Open-Meteo")
    plt.xlabel("Date and Time")
    plt.ylabel("Values")
    plt.legend()
    plt.grid(True)
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

# Función principal para la interfaz
def main():
    st.title("Weather Data Visualizer")
    uploaded_file = st.file_uploader("Upload CSV or JSON file", type=["csv", "json"])
    
    if uploaded_file:
        data = read_weather_data(uploaded_file)
        if not data.empty:
            data = clean_data(data)
            
            st.write("Cleaned Data:")
            st.dataframe(data)
            
            if st.button("Show Scatter Plot"):
                plot_scatter(data)
            if st.button("Show Line Chart"):
                plot_line(data)
    # Obtener datos desde una API
    st.subheader("Obtener datos desde una API")
    api_key = st.text_input("Ingresa tu API Key de OpenWeatherMap", type="password")
    city = st.text_input("Ingresa el nombre de la ciudad")
    
    if st.button("Obtener datos del clima"):
        if api_key and city:
            weather_data = fetch_weather_data(api_key, city)
            if weather_data:
                st.write("Datos obtenidos de la API:")
                st.json(weather_data)
            else:
                st.error("No se pudieron obtener los datos. Verifica la ciudad o la API Key.")
        else:
            st.warning("Por favor, ingresa una API Key válida y el nombre de la ciudad.")
    
    st.title("Historical Weather Data Viewer (Open-Meteo)")
    latitude = st.number_input("Latitud", value=0.0, format="%.6f")
    longitude = st.number_input("Longitud", value=0.0, format="%.6f")
    start_date = st.date_input("Fecha de inicio")
    end_date = st.date_input("Fecha de fin")

    if st.button("Obtener datos históricos"):
        if latitude and longitude and start_date and end_date:
            start_date_dt = datetime.combine(start_date, datetime.min.time())
            end_date_dt = datetime.combine(end_date, datetime.min.time())
            st.info("Obteniendo datos históricos...")
            data = fetch_open_meteo_data(latitude, longitude, start_date_dt, end_date_dt)
            if data:
                df = process_open_meteo_data(data)
                st.write("Datos obtenidos:")
                st.dataframe(df)

                # Mostrar gráficos
                st.write("Gráficos de temperatura y humedad:")
                st.line_chart(df.set_index("date")[["temperature", "humidity"]])
            else:
                st.error("No se pudieron obtener los datos históricos. Verifica los parámetros.")
        else:
            st.warning("Por favor, completa todos los campos.")


if __name__ == '__main__':
    main()
