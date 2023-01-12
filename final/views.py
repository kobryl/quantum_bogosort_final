import json
import requests
from . import secret
from urllib.request import urlopen

from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse

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
    context = {'stops': Stop.objects.all()}
    print(calculate_estimated_travel_time((54.354656, 18.652203), (54.365726, 18.621069)))
    return render(request, 'final/index.html', context)


def tf(request, tf_id):
    tf = get_object_or_404(Tf, pk=tf_id)
    return render(request, 'final/tf.html', {'tf': tf})


def trasa(request):
    return render(request, 'final/trasa.html')


def calculate_estimated_travel_time(positionA, positionB):
    url = "https://dev.virtualearth.net/REST/v1/Routes/DistanceMatrix?origins="
    url += str(positionA[0]) + "," + str(positionA[1]) + "&destinations="
    url += str(positionB[0]) + "," + str(positionB[1]) + "&travelMode=walking&key="
    url += secret.SECRET_KEY

    response = requests.get(url)
    data = response.json()
    time = float(data["resourceSets"][0]["resources"][0]["results"][0]["travelDuration"])/1.5
    return time