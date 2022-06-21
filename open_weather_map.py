import requests
from functools import cache
from datetime import datetime


class OpenWeatherMap:
    API_KEY = open("openweathermap_api_key", "r").read()
    URL = "https://api.openweathermap.org"

    def __init__(self, city: str):
        self.city = city

    @property
    @cache
    def geocoding(self) -> tuple:
        url = f"{self.URL}/geo/1.0/direct?q={self.city}&appid={self.API_KEY}"
        response = requests.get(url).json()
        name, lat, lon = response[0]["name"], response[0]["lat"], response[0]["lon"]
        return name, lat, lon

    def get_weather(self) -> dict:
        _, lat, lon = self.geocoding
        url = f"{self.URL}/data/2.5/weather?lat={lat}&lon={lon}&appid={self.API_KEY}"
        response = requests.get(url).json()

        description = response["weather"][0]["description"]
        temperate_celsius = self.__kelvin_to_celsius(response["main"]["temp"])
        temperate_farenheit = self.__kelvin_to_farenheit(response["main"]["temp"])
        feels_like_celsius = self.__kelvin_to_celsius(response["main"]["feels_like"])
        feels_like_farenheit = self.__kelvin_to_farenheit(response["main"]["feels_like"])
        sunrise_time = datetime.utcfromtimestamp(response["sys"]["sunrise"] + response["timezone"]).isoformat()
        sunset_time = datetime.utcfromtimestamp(response["sys"]["sunset"] + response["timezone"]).isoformat()
        humidity = response["main"]["humidity"]
        wind_seed = response["wind"]["speed"]
        visibility = response["visibility"]

        temperature = dict(celsius=round(temperate_celsius, 2), farenheit=round(temperate_farenheit, 2))
        feels_like = dict(celsius=round(feels_like_celsius, 2), farenheit=round(feels_like_farenheit, 2))

        return dict(description=description, temperature=temperature, feels_like=feels_like, humidity=humidity, sunrise_time=sunrise_time, sunset_time=sunset_time, wind_speed=wind_seed, visibility=visibility)

    def get_solar_radiation(self):
        url = f"https://api.openweathermap.org/data/2.5/weather?q={self.city}&appid={self.api_key}"
        response = requests.get(url).json()
        return response

    def __kelvin_to_celsius(self, kelvin: float) -> float:
        return kelvin - 273.15

    def __kelvin_to_farenheit(self, kelvin: float) -> float:
        return (kelvin - 273.15) * 9/5 + 32