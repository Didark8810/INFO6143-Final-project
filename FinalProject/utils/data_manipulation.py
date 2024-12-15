import pandas as pd

def data_preparation(data, option):
    '''Prepares data by converting it, removing duplicates, and handling missing values.'''
    try:
        data_cn = convert_df(data, option)

        # Removing duplicates
        df_nd = data_cn.drop_duplicates()

        # Handling missing values
        df_nm = df_nd.dropna()

        return df_nm
    except Exception as e:
        print("data_manipulation.data_preparation - Error: ", e)

def convert_df(data, option):
    '''Converts raw weather data into a DataFrame based on the selected option.'''
    if option == 1:
        try:
            return pd.DataFrame({'Temperature': [data["current"]["temperature_2m"]], 
                                'Feels like': [data["current"]["apparent_temperature"]],
                                'Humidity': [data["current"]["relative_humidity_2m"]], 
                                'Precipitation': [data["current"]["precipitation"]]})
        except Exception as e:
            print("data_manipulation.convert_df - Error - option 1: ", e)
    elif option == 2:
        try:
            return pd.DataFrame({'Date': data["daily"]["time"], 
                                'Max Temperature': data["daily"]["temperature_2m_max"],
                                'Min Temperature': data["daily"]["temperature_2m_min"], 
                                'Precipitation': data["daily"]["precipitation_sum"]})
        except Exception as e:
            print("data_manipulation.convert_df - Error - option 2: ", e)
    elif option == 3:
        try:
            return pd.DataFrame({'Date': data["daily"]["time"], 
                                'Temperature': data["daily"]["temperature_2m_max"],
                                'Feels like': data["daily"]["temperature_2m_min"], 
                                'Humidity': data["daily"]["precipitation_sum"], 
                                'Precipitation': data["daily"]["precipitation_sum"]})
        except Exception as e:
            print("data_manipulation.convert_df - Error - option 2: ", e)

def rename_data_2_save(data):
    '''Renames columns in the DataFrame to standardize them for saving.'''
    return data.rename(columns={
        "Max Temperature":"temperature",
        "Date":"date",
        "Precipitation":"humidity"
    })