import matplotlib.pyplot as plt
import pandas as pd
import streamlit as st

def date_range_plot(data, option):
  try:    
    # Streamlit app
    st.title("Weather Data")

    # Plotting the data
    fig, ax = plt.subplots()
    if option == 'Max Temperature':
      ax.plot(data['Date'], data['Max Temperature'], label='Temperature (°C)', color='tab:red')
      ax.set_ylabel('Max Temperature')
    elif option == 'Precipitation':
      ax.plot(data['Date'], data['Precipitation'], label='Precipitation', color='tab:blue')
      ax.set_ylabel('Precipitation')
    elif option == 'Min Temperature':
      ax.plot(data['Date'], data['Min Temperature'], label='Temperature (°C)', color='tab:orange')
      ax.set_ylabel('Min Temperature')
    elif option == 'Temperature':
      ax.plot(data['Date'], data['Max Temperature'], label='Max Temperature (°C)', color='tab:red', marker='o')
      ax.plot(data['Date'], data['Min Temperature'], label='Min Temperature (°C)', color='tab:orange', marker='o')
      ax.set_ylabel('Temperature')

    ax.set_xlabel('Date')
    plt.xticks(rotation=90)  # Rotate x-axis labels to be vertical
    ax.legend()

    # Display the plot 
    st.pyplot(fig)
  except Exception as e:
    print("plot.date_range_plot - Error: ", e)

def current_weather_show(data):
    try:
        st.subheader("Current Weather")
        st.write(f"**Temperature:** {data['Temperature'][0]} °C")
        st.write(f"**Feels like (°C):** {data['Feels like'][0]} %")
        st.write(f"**Humidity (%):** {data['Humidity'][0]} km/h")
        st.write(f"**Precipitation:** {data['Precipitation'][0]}°")
    except Exception as e:
        print("plot.current_weather_show - Error: ", e)

def current_weather_plot(data):
  try:
    st.subheader("Current Weather")
    metric = ['Temperature (°C)', 'Feels like (°C)', 'Humidity (%)', 'Precipitation']
    data = [data['Temperature'][0], 
            data['Feels like'][0],
            data['Humidity'][0],
            data['Precipitation'][0]]

    # Plot the data
    fig, ax = plt.subplots()
    ax.barh(metric, data, color='skyblue')
    ax.set_xlabel('Value')
    ax.set_title('Current Weather')
    st.pyplot(fig)
  except Exception as e:
    print("plot.current_weather_plot - Error: ", e)