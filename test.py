from datetime import datetime


from open_weather_map import OpenWeatherMap


CITY = "Lisbon"
response = OpenWeatherMap(CITY).get_weather()


def kelvin_to_celsius(kelvin):
    return kelvin - 273.15

def kelvin_to_farenheit(kelvin):
    return (kelvin - 273.15) * 9/5 + 32


temperate_celsius = kelvin_to_celsius(response["main"]["temp"])
temperate_farenheit = kelvin_to_farenheit(response["main"]["temp"])

print(temperate_celsius, temperate_farenheit)

feels_like_celsius = kelvin_to_celsius(response["main"]["feels_like"])
feels_like_farenheit = kelvin_to_farenheit(response["main"]["feels_like"])

print(feels_like_celsius, feels_like_farenheit)

humidity = response["main"]["humidity"]

print(humidity)

description = response["weather"][0]["description"]

print(description)

sunrise_time = datetime.utcfromtimestamp(response["sys"]["sunrise"] + response["timezone"]).isoformat()
sunset_time = datetime.utcfromtimestamp(response["sys"]["sunset"] + response["timezone"]).isoformat()

print(sunrise_time, sunset_time)

wind_speed = response["wind"]["speed"]

print(wind_speed)

visibility = response["visibility"]

print(visibility)