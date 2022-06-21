import json


from router import Router
from open_weather_map import OpenWeatherMap


def temperature(city: str):
    temperature = OpenWeatherMap(city).get_temperature()
    return {"statusCode": 200, "body": json.dumps(temperature)}


def feels_like(city: str):
    feels_like = OpenWeatherMap(city).get_feels_like()
    return {"statusCode": 200, "body": json.dumps(feels_like)}


def wind(city: str):
    wind = OpenWeatherMap(city).get_wind()
    return {"statusCode": 200, "body": json.dumps(wind)}


def humidity(city: str):
    humidity = OpenWeatherMap(city).get_humidity()
    return {"statusCode": 200, "body": json.dumps(humidity)}


def visibility(city: str):
    visibility = OpenWeatherMap(city).get_visibility()
    return {"statusCode": 200, "body": json.dumps(visibility)}


def sun(city: str):
    sun = OpenWeatherMap(city).get_sun()
    return {"statusCode": 200, "body": json.dumps(sun)}


router = Router()
router.set(path="/temperature", method="GET", handler=temperature)
router.set(path="/feels_like", method="GET", handler=feels_like)
router.set(path="/wind", method="GET", handler=wind)
router.set(path="/humidity", method="GET", handler=humidity)
router.set(path="/visibility", method="GET", handler=visibility)
router.set(path="/sun", method="GET", handler=sun)


def lambda_handler(event, context):
    path = event["requestContext"]["http"]["path"]
    method = event["requestContext"]["http"]["method"]
    query_string = event["queryStringParameters"]

    if "city" not in query_string:
        return {"statusCode": 400, "body": json.dumps({"message": "city is required!"})}

    city = event["queryStringParameters"]["city"]
    func = router.get(path=path, method=method)
    return func(city=city)
