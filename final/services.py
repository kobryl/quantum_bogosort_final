import datetime
import json
from time import strftime
from urllib.request import urlopen

import datetime
import json
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


def get_today():
    return datetime.datetime.today().isoformat()[0:10]


def get_possible_routes(stop1, stop2):
    url = "https://ckan.multimediagdansk.pl/dataset/c24aa637-3619-4dc2-a171-a23eec8f2172/resource/3115d29d-b763-4af5-93f6-763b835967d6/download/stopsintrip.json"
    response = urlopen(url)
    data_json = json.loads(response.read())
    today = get_today()
    var = data_json[today]['stopsInTrip']
    stop1routes = []
    stop2routes = []
    for i in var:
        if i['stopId'] == stop1:
            stop1routes.append(i)
        elif i['stopId'] == stop2:
            stop2routes.append(i)
    routes = []
    for i in stop1routes:
        if i in stop2routes and i['routeId'] not in routes \
                and i['stopSequence'] < stop2routes[stop2routes.index(i)]['stopSequence']:
            routes.append(i['routeId'])
    return routes


def get_route_number_by_id(route_id):
    url = "https://ckan.multimediagdansk.pl/dataset/c24aa637-3619-4dc2-a171-a23eec8f2172/resource/22313c56-5acf-41c7-a5fd-dc5dc72b3851/download/routes.json"
    response = urlopen(url)
    data_json = json.loads(response.read())
    routes = data_json[get_today()]['routes']
    for route in routes:
        if route['routeId'] == route_id:
            return route['routeShortName']
    return ''


def get_data_from_json(url):
    response = urlopen(url)
    data_json = json.loads(response.read())
    return data_json
