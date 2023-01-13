from . import services
from django.shortcuts import render, redirect
from .models import Stop, Route


def index(request):
    incidents = services.get_info_about_incidents()
    stops_dict = services.get_serialized_stop_info()
    context = {'stops': Stop.objects.all().order_by('stopName', 'subName'), 'stops_dict': stops_dict,
               'incidents': incidents}
    return render(request, 'final/index.html', context)


def create_path(request):
    if request.method == 'POST':
        start = request.POST['starting-route']
        end = request.POST['ending-route']
        s1 = Stop.objects.get(stopId=start)
        s2 = Stop.objects.get(stopId=end)
        start_name = s1.stopName + " " + s1.subName
        end_name = s2.stopName + " " + s2.subName
        max_changes = request.POST['max_changes']
        max_waiting_time = request.POST['max_waiting_time']
        max_distance_on_foot = request.POST['max_distance_on_foot']
        context = services.create_path(start, end, max_changes, max_waiting_time, max_distance_on_foot)
        return render(request, 'final/trasa.html', context)
    return render(request, 'final/index.html')