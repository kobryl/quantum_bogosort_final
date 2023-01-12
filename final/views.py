from . import services
from django.shortcuts import render, redirect
from django.core import serializers
from .models import Stop, Route
from .services import get_possible_routes



def index(request):
    url = 'https://ckan.multimediagdansk.pl/dataset/c24aa637-3619-4dc2-a171-a23eec8f2172/resource/d3e96eb6-25ad-4d6c' \
          '-8651-b1eb39155945/download/stopsingdansk.json'
    data_json = services.get_data_from_json(url)
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
    print(Stop.objects.all())
    stops_dict = serializers.serialize('python', Stop.objects.all())
    context = {'stops': Stop.objects.all().order_by('stopName', 'subName'), 'stops_dict': stops_dict}
    get_possible_routes(2018, 2016)
    return render(request, 'final/index.html', context)


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
    route = []
    for _ in _:
        stop1 = Stop.objects.get(stopId=_['stop1'])
        stop2 = Stop.objects.get(stopId=_['stop2'])
        best_route = find_transport_with_fastest_arrival_time(stop1, stop2)
        line = services.get_route_number_by_id(best_route)
        route.append(Route.objects.create(stop1=stop1, stop2=stop2, line=line))
    context = {'start_id': start_id, 'end_id': end_id, 'max_changes': max_changes,
               'max_waiting_time': max_waiting_time, 'max_distance_on_foot': max_distance_on_foot,
               'start_name': start_name, 'end_name': end_name, 'route': route}
    return render(request, 'final/trasa.html', context)
