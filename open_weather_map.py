import requests
from functools import cache


class OpenWeatherMap:
    API_KEY = open("openweathermap_api_key", "r").read()
    URL = "https://api.openweathermap.org"

    def __init__(self, city: str):
        self.city = city

    @property
    @cache
    def geocoding(self):
        url = f"{self.URL}/geo/1.0/direct?q={self.city}&appid={self.API_KEY}"
        response = requests.get(url).json()
        return response[0]["name"], response[0]["lat"], response[0]["lon"]

    def get_weather(self):
        _, lat, lon = self.geocoding
        url = f"{self.URL}/data/2.5/weather?lat={lat}&lon={lon}&appid={self.API_KEY}"
        response = requests.get(url).json()
        return response

    def get_solar_radiation(self):
        url = f"https://api.openweathermap.org/data/2.5/weather?q={self.city}&appid={self.api_key}"
        response = requests.get(url).json()
        return response

    def kelvin_to_celsius(kelvin: float) -> float:
        return kelvin - 273.15

    def kelvin_to_farenheit(kelvin: float) -> float:
        return (kelvin - 273.15) * 9/5 + 32