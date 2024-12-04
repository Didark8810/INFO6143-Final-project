import streamlit as st
from datetime import datetime, timedelta
import utils.api_consumption as api
import utils.plot as pl
import utils.data_manipulation as dm
import utils.csv as csv

def init():
    #working with csv data
    st.title("Weather Data Visualizer with Python")
    st.write("**Option # 1: Local CSV**")
    uploaded_file = st.file_uploader("Upload CSV file", type=["csv"])
    
    if uploaded_file:
        data = csv.read_weather_data(uploaded_file)
        if not data.empty:
            data = csv.clean_data(data)
            
            st.write("Cleaned Data:")
            st.dataframe(data)
            csv.plot_line(data)
            # if st.button("Show Line Chart Temp/Humidity vs time"):
            #     csv.plot_line(data)
            # if st.button("Show Scatter Plot Temp vs Humidity"):
            #     csv.plot_scatter(data)
            

    # Define the options to plot
    st.write("**Option # 2: Online**")
    option = st.selectbox(
        'Select your plot:',
        ('','Specific Date', 'Range of dates')
    )

    # 
    if option == 'Specific Date':
        date_init = st.text_input("Input a date (YYYY-MM-DD):")
        
        
        
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("Today"):    
                try:
                    data = api.get_current_weather()
                    if data:
                        data_cl = dm.data_preparation(data, 1)
                        pl.current_weather_show(data_cl)
                        #pl.current_weather_plot(data_cl)
                except:
                    st.error("view.init - Error to get data. Please check data format (YYYY-MM-DD) or API availability.")
            
        
            
        with col2:
            if st.button("Search"):
                try:
                    data = api.get_weather_date_range(date_init,date_init)
                    if data:
                        data_cl = dm.data_preparation(data, 3)
                        pl.current_weather_show(data_cl)
                        #pl.current_weather_plot(data_cl)
                except:
                    st.error("view.init - Error to get data. Please check data format (YYYY-MM-DD) or API availability.")
        
    elif option == 'Range of dates':
        date_init = st.text_input("Input an initial date (YYYY-MM-DD):")
        date_end = st.text_input("Input a final date (YYYY-MM-DD):")
        if date_init and date_end:
            try:
                datetime.strptime(date_init, '%Y-%m-%d')
                datetime.strptime(date_end, '%Y-%m-%d')
                data = api.get_weather_date_range(date_init, date_end)
                if data:
                    data_cl = dm.data_preparation(data, 2)
                    # Select option to plot
                    option = st.selectbox(
                        'Select the data you want to plot:',
                        ('Max Temperature', 'Min Temperature', 'Precipitation', 'Temperature')
                    )
                    pl.date_range_plot(data_cl, option)
            except:
                st.error("view.init - Error to get data. Please check data format (YYYY-MM-DD) or API availability.")