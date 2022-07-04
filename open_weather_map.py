import json
import logging
from urllib.request import Request, urlopen, URLError, HTTPError
from functools import cache
from datetime import datetime


log = logging.getLogger(__name__)
log_level = "INFO"


class OpenWeatherMap:
    API_KEY = open("openweathermap_api_key", "r").read()
    URL = "https://api.openweathermap.org"

    def __init__(self, city: str):
        self.city = city

    @property
    @cache
    def geocoding(self) -> tuple:
        url = f"{self.URL}/geo/1.0/direct?q={self.city}&appid={self.API_KEY}"
        response = self.__make_request(url)
        lat, lon = response[0]["lat"], response[0]["lon"]
        return lat, lon

    @property
    @cache
    def weather(self) -> dict:
        lat, lon = self.geocoding
        url = f"{self.URL}/data/2.5/weather?lat={lat}&lon={lon}&appid={self.API_KEY}"
        weather = self.__make_request(url)
        return weather

    def get_temperature(self) -> dict:
        feels_like = self.weather["main"]["feels_like"]
        celsius = round(self.__kelvin_to_celsius(feels_like), 2)
        farenheit = round(self.__kelvin_to_farenheit(feels_like), 2)
        return dict(celsius=celsius, farenheit=farenheit)

    def get_feels_like(self) -> dict:
        temp = self.weather["main"]["temp"]
        celsius = round(self.__kelvin_to_celsius(temp), 2)
        farenheit = round(self.__kelvin_to_farenheit(temp), 2)
        return dict(celsius=celsius, farenheit=farenheit)

    def get_wind(self) -> dict:
        wind = self.weather["wind"]
        return dict(speed=wind["speed"], deg=wind["deg"], gust=wind["gust"])

    def get_humidity(self) -> dict:
        humidity = self.weather["main"]["humidity"]
        return dict(humidity=humidity)

    def get_visibility(self) -> dict:
        visibility = self.weather["visibility"]
        return dict(visibility=visibility)

    def get_sun(self) -> dict:
        weather = self.weather
        sys, timezone = weather["sys"], weather["timezone"]
        sunrise = datetime.utcfromtimestamp(sys["sunrise"] + timezone).isoformat()
        sunset = datetime.utcfromtimestamp(sys["sunset"] + timezone).isoformat()
        return dict(sunrise=sunrise, sunset=sunset)

    @staticmethod
    def __make_request(url: str) -> dict:
        request = Request(url)
        log.info(f"Starting request to {url}")

        try:
            response = urlopen(request)
            body = response.read()
            try:
                return json.loads(body)
            except ValueError:
                return body

        except HTTPError as e:
            log.error(f"Request failed: {e.code} {e.reason}")
        except URLError as e:
            log.error(f"Server connection failed: {e.reason}")

    def __kelvin_to_celsius(self, kelvin: float) -> float:
        return kelvin - 273.15

    def __kelvin_to_farenheit(self, kelvin: float) -> float:
        return (kelvin - 273.15) * 9/5 + 32
