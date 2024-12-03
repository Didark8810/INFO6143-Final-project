import streamlit as st
from datetime import datetime, timedelta
import utils.api_consumption as api
import utils.plot as pl
import utils.data_manipulation as dm

def init():
    # Define the options to plot
    option = st.selectbox(
        'Select your plot:',
        ('','Today', 'Specific Date', 'Range of dates')
    )

    # 
    if option == 'Today':
        try:
            data = api.get_current_weather()
            if data:
                data_cl = dm.data_preparation(data, 1)
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