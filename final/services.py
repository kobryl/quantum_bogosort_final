import datetime
import json
from time import strftime
from urllib.request import urlopen

from . import secret
import requests


def calculate_estimated_travel_time(positionA, positionB):
    url = "https://dev.virtualearth.net/REST/v1/Routes/DistanceMatrix?origins="
    url += str(positionA[0]) + "," + str(positionA[1]) + "&destinations="
    url += str(positionB[0]) + "," + str(positionB[1]) + "&travelMode=walking&key="
    url += secret.SECRET_KEY

    response = requests.get(url)
    data = response.json()
    if data["statusCode"] >= 300:
        return -1

    print(data)
    time = float(data["resourceSets"][0]["resources"][0]["results"][0]["travelDuration"]) / 1.5
    return time


def get_data_from_json(url):
    response = urlopen(url)
    data_json = json.loads(response.read())
    return data_json
