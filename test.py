from open_weather_map import OpenWeatherMap


CITY = "Lisbon"
weather = OpenWeatherMap(CITY).get_weather()


print(weather)
