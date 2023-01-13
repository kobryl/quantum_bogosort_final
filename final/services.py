import json
import requests
from django.shortcuts import render, redirect
from django.core import serializers
from urllib.request import urlopen
from .models import Stop
from . import secret


def calculate_estimated_travel_time(positionA, positionB):
    url = "https://dev.virtualearth.net/REST/v1/Routes/DistanceMatrix?origins="
    url += str(positionA[0]) + "," + str(positionA[1]) + "&destinations="
    url += str(positionB[0]) + "," + str(positionB[1]) + "&travelMode=walking&key="
    url += secret.SECRET_KEY

    response = requests.get(url)
    data = response.json()
    if data["statusCode"] >= 300:
        return -1

    time = float(data["resourceSets"][0]["resources"][0]["results"][0]["travelDuration"]) / 1.5
    return time


def get_data_from_json(url):
    response = urlopen(url)
    data_json = json.loads(response.read())
    return data_json


def get_info_about_incidents():
    url = 'https://files.cloudgdansk.pl/d/otwarte-dane/ztm/bsk.json'
    info = get_data_from_json(url)["komunikaty"]
    return info


def get_info_about_stop(stopIdList):
    url = 'https://ckan.multimediagdansk.pl/dataset/c24aa637-3619-4dc2-a171-a23eec8f2172/resource/d3e96eb6-25ad-4d6c' \
          '-8651-b1eb39155945/download/stopsingdansk.json'
    info = get_data_from_json(url)["stops"]
    result = []
    for i in range(len(info)):
        if info[i]["stopId"] in stopIdList:
            result.append(info[i]["stopDesc"] + " " + info[i]["subName"])
    return result


def get_serialized_stop_info():
    url = 'https://ckan.multimediagdansk.pl/dataset/c24aa637-3619-4dc2-a171-a23eec8f2172/resource/d3e96eb6-25ad-4d6c' \
          '-8651-b1eb39155945/download/stopsingdansk.json'
    data_json = get_data_from_json(url)
    ids = Stop.objects.all().values_list('stopId', flat=True)
    if Stop.lastUpdate is not None and Stop.lastUpdate < data_json['lastUpdate']:
        Stop.objects.all().delete()
        ids = []
        Stop.lastUpdate = data_json['lastUpdate']

    for stop in data_json['stops']:
        if stop['nonpassenger'] is False:
            if Stop.lastUpdate or stop['stopId'] not in ids:
                Stop.objects.create(stopId=stop['stopId'], stopName=stop['stopName'], subName=stop['subName'],
                                    stopLat=stop['stopLat'], stopLon=stop['stopLon'], nonpassenger=stop['nonpassenger'])

    stops_dict = serializers.serialize('python', Stop.objects.all())
    return stops_dict


#TODO to dokończyć jak olek skończy
def trasa():
    if request.method == 'GET':
        return redirect('final:index')
    start_id = request.POST['start']
    start_name = Stop.objects.get(stopId=start_id).stopName + ' ' + Stop.objects.get(stopId=start_id).subName
    end_id = request.POST['end']
    end_name = Stop.objects.get(stopId=end_id).stopName + ' ' + Stop.objects.get(stopId=end_id).subName
    max_changes = request.POST['max_changes']
    max_waiting_time = request.POST['max_waiting_time']
    max_distance_on_foot = request.POST['max_distance_on_foot']
    # tu bedzie komunikacja z algorytmem
    route = []
    #for _ in _:
    #    stop1 = Stop.objects.get(stopId=_['stop1'])
    #    stop2 = Stop.objects.get(stopId=_['stop2'])
        #best_route = find_transport_with_fastest_arrival_time(stop1, stop2)
        #algo olka tf. Później odkomentować i ogarnąć
        #line = services.get_route_number_by_id(best_route)
        #route.append(Route.objects.create(stop1=stop1, stop2=stop2, line=line))
    context = {'start_id': start_id, 'end_id': end_id, 'max_changes': max_changes,
               'max_waiting_time': max_waiting_time, 'max_distance_on_foot': max_distance_on_foot,
               'start_name': start_name, 'end_name': end_name, 'route': route}
    return render(request, 'final/trasa.html', context)


#def get_time():
#    date = datetime.datetime.now()
#    return strftime("%H:%M")
#def get_today():
#    return datetime.datetime.today().isoformat()[0:10]
#def get_possible_routes(stop1, stop2):
#    url = "https://ckan.multimediagdansk.pl/dataset/c24aa637-3619-4dc2-a171-a23eec8f2172/resource/3115d29d-b763-4af5-93f6-763b835967d6/download/stopsintrip.json"
#    response = urlopen(url)
#    data_json = json.loads(response.read())
#    today = get_today()
#    var = data_json[today]['stopsInTrip']
#    stop1routes = []
#    stop2routes = []
#    for i in var:
#        if i['stopId'] == stop1:
#            stop1routes.append(i)
#        elif i['stopId'] == stop2:
#            stop2routes.append(i)
#    routes = []
#    for i in stop1routes:
#        for j in stop2routes:
#            if i['routeId'] not in routes and i['routeId'] == j['routeId'] and i['stopSequence'] < j['stopSequence']:
#                routes.append(i['routeId'])
#                stop2routes.remove(j)
#    return routes
#def get_route_number_by_id(route_id):
#    url = "https://ckan.multimediagdansk.pl/dataset/c24aa637-3619-4dc2-a171-a23eec8f2172/resource/22313c56-5acf-41c7-a5fd-dc5dc72b3851/download/routes.json"
#    response = urlopen(url)
#    data_json = json.loads(response.read())
#    routes = data_json[get_today()]['routes']
#    for route in routes:
#        if route['routeId'] == route_id:
#            return route['routeShortName']
#    return ''
#def find_transport_routeId_with_fastest_arrival_time(stop, destination):
#    departures = []
#    departures_routeId = []
#    routes = get_possible_routes(stop, destination)
#    url = 'http://ckan2.multimediagdansk.pl/departures?stopId=' + str(stop)
#    json_data = get_data_from_json(url)
#    data = json_data["departures"]
#    if len(data) == 0:
#        return 0
#    departures.append(data[0]["estimatedTime"][11:19])
#    departures_routeId.append(data[0]["routeId"])
