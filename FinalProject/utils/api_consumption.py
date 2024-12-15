import requests

def get_weather_date_range(start_date, end_date):
  '''Fetches weather data for a specified date range from the Open-Meteo API.'''
  try:
    # Define the base URL for the Open-Meteo API
    base_url = "https://api.open-meteo.com/v1/forecast"

    # Latitude and longitude of London, Ontario
    latitude = "42.98" 
    longitude = "-81.23"

    # Make the API request
    URL = base_url + "?latitude=" + latitude + "&longitude=" + longitude + "&daily=temperature_2m_max,temperature_2m_min,precipitation_sum&timezone=America%2FNew_York" + "&start_date=" + start_date + "&end_date=" + end_date
    response = requests.get(URL)
    
    # Parse the JSON response
    weather_data = response.json()

    # return weather data
    return weather_data
  except:
    print('api_consumption.get_weather_date_range - Error in gettin data')

def get_current_weather():
  '''Fetches the current weather data from the Open-Meteo API.'''
  try:
    # Define the base URL for the Open-Meteo API
    base_url = "https://api.open-meteo.com/v1/forecast"

    # Llatitude and longitude of London, Ontario
    latitude = "42.98" 
    longitude = "-81.23"

    # Make the API request
    URL = base_url + "?latitude=" + latitude + "&longitude=" + longitude + "&current=temperature_2m,relative_humidity_2m,apparent_temperature,precipitation&timezone=America%2FNew_York"
    response = requests.get(URL)
    
    # Parse the JSON response
    weather_data = response.json()

    #return weather data
    return weather_data
  except:
    print('api_consumption.get_current_weather - Error in gettin data')