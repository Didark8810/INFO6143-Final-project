import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st
import requests

# Leer un archivo CSV
def load_weather_data(file_path):
    try:
        data = pd.read_csv(file_path)
        print("Datos cargados exitosamente.")
        return data
    except FileNotFoundError:
        print("Archivo no encontrado. Por favor, verifica la ruta.")
    except pd.errors.EmptyDataError:
        print("El archivo está vacío.")
    except Exception as e:
        print(f"Error al cargar el archivo: {e}")
        return None

# Guardar datos en CSV
def save_weather_data(data, file_path):
    try:
        data.to_csv(file_path, index=False)
        print(f"Datos guardados en {file_path}.")
    except Exception as e:
        print(f"Error al guardar los datos: {e}")

# Manejo de datos faltantes
def handle_missing_data(data):
    data.fillna(data.mean(), inplace=True)
    return data

# Graficar temperatura a lo largo del tiempo
def plot_temperature(data):
    plt.figure(figsize=(10, 6))
    plt.plot(data['date'], data['temperature'], marker='o', label='Temperature')
    plt.xlabel('Date')
    plt.ylabel('Temperature (°C)')
    plt.title('Temperature Over Time')
    plt.legend()
    plt.grid()
    plt.show()

# Gráfico de dispersión (Humedad vs Temperatura)
def scatter_humidity_temperature(data):
    plt.figure(figsize=(8, 6))
    plt.scatter(data['temperature'], data['humidity'], alpha=0.6, c='blue')
    plt.xlabel('Temperature (°C)')
    plt.ylabel('Humidity (%)')
    plt.title('Humidity vs Temperature')
    plt.grid()
    plt.show()

# Obtener datos desde una API
def fetch_weather_data(api_key, city):
    #https://openweathermap.org/history
    #05773f69315d38dbaa3535df8bb04ff9       key
    url = f"https://history.openweathermap.org/data/2.5/history/city?q=London,UK&appid={api_key}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error: {response.status_code}")
        return None

# Interfaz interactiva con Streamlit
def main():
    st.title("Weather Data Visualizer")
    
    # Subir archivo
    uploaded_file = st.file_uploader("Sube tu archivo CSV", type=["csv"])
    if uploaded_file:
        data = pd.read_csv(uploaded_file)
        st.write("Datos cargados:")
        st.dataframe(data)

        # Manejo de datos faltantes
        #data = handle_missing_data(data)

        # Graficar temperatura
        if st.button("Visualizar temperatura"):
            st.write("Gráfico de temperatura:")
            st.line_chart(data['temperature'])
        
        # Graficar scatter (Humedad vs Temperatura)
        if st.button("Gráfico de dispersión (Humedad vs Temperatura)"):
            st.write("Scatter Plot:")
            scatter_humidity_temperature(data)

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

if __name__ == "__main__":
    main()
