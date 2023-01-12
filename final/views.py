import json
from urllib.request import urlopen

from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse

from .models import Tf, MainForm


# Create your views here.


def index(request):
    url = 'https://ckan.multimediagdansk.pl/dataset/c24aa637-3619-4dc2-a171-a23eec8f2172/resource/d3e96eb6-25ad-4d6c-8651-b1eb39155945/download/stopsingdansk.json'
    response = urlopen(url)
    data_json = json.loads(response.read())
    ids = MainForm.objects.all().values_list('stopId', flat=True)
    if MainForm.lastUpdate is not None and MainForm.lastUpdate < data_json['lastUpdate']:
        MainForm.objects.all().delete()
        ids = []
        MainForm.lastUpdate = data_json['lastUpdate']
    for stop in data_json['stops']:
        if stop['nonpassenger'] is False:
            if MainForm.lastUpdate or stop['stopId'] not in ids:
                MainForm.objects.create(stopId=stop['stopId'], stopName=stop['stopName'], subName=stop['subName'],
                                        stopLat=stop['stopLat'], stopLon=stop['stopLon'], nonpassenger=stop['nonpassenger'])
    context = {'stops': MainForm.objects.all()}
    return render(request, 'final/index.html', context)


def tf(request, tf_id):
    tf = get_object_or_404(Tf, pk=tf_id)
    return render(request, 'final/tf.html', {'tf': tf})


def trasa(request):
    return render(request, 'final/trasa.html')
