from . import services
from django.shortcuts import render, redirect
from .models import Stop


def index(request):
    incidents = services.get_info_about_incidents()
    stops_dict = services.get_serialized_stop_info()
    context = {'stops': Stop.objects.all().order_by('stopName', 'subName'), 'stops_dict': stops_dict,
               'incidents': incidents}
    return render(request, 'final/index.html', context)


def trasa(request):
    if request.method == 'POST':
        start = request.POST['starting-route']
        end = request.POST['ending-route']
        max_changes = request.POST['max_changes']
        max_waiting_time = request.POST['max_waiting_time']
        max_distance_on_foot = request.POST['max_distance_on_foot']
        services.trasa(start, end, max_changes, max_waiting_time, max_distance_on_foot)
    return render(request, 'final/index.html')