import requests
   
API_KEY = "563a4d5c4e7b82501914de02304217ed"

def get_weather(city):
    """Fetch weather data for a city from OpenWeatherMap API."""
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
    response = requests.get(url)

    #print(response.json())
    if response.status_code == 200:
        data = response.json()
        weather = data["weather"][0]["description"]
        temp = data["main"]["temp"]
        return f"The weather in {city} is {weather} with a temperature of {temp}°C."
    elif response.status_code == 404:      return "City not found. Please check the spelling."
    else:
        return "Sorry, I couldn't retrieve the weather information right now."

