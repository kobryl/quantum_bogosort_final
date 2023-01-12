import json
import requests
from . import secret
from urllib.request import urlopen

from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.core import serializers

from .models import Stop


# Create your views here.


def index(request):
    url = 'https://ckan.multimediagdansk.pl/dataset/c24aa637-3619-4dc2-a171-a23eec8f2172/resource/d3e96eb6-25ad-4d6c-8651-b1eb39155945/download/stopsingdansk.json'
    response = urlopen(url)
    data_json = json.loads(response.read())
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
    context = {'stops': Stop.objects.all().order_by('stopName', 'subName'), 'stops_dict': stops_dict}
    return render(request, 'final/index.html', context)

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
    time = float(data["resourceSets"][0]["resources"][0]["results"][0]["travelDuration"])/1.5
    return time

def trasa(request):
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
    context = {'start_id': start_id, 'end_id': end_id, 'max_changes': max_changes,
               'max_waiting_time': max_waiting_time, 'max_distance_on_foot': max_distance_on_foot,
               'start_name': start_name, 'end_name': end_name, 'route': []}
    return render(request, 'final/trasa.html', context)
