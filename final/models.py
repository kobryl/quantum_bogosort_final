import json
from urllib.request import urlopen

from django.contrib.sites import requests
from django.db import models

# Create your models here.

class Stop(models.Model):
    lastUpdate = None
    stopId = models.IntegerField(primary_key=True)
    stopName = models.CharField(max_length=200)
    subName = models.CharField(max_length=200)
    stopLat = models.FloatField()
    stopLon = models.FloatField()
    nonpassenger = models.BooleanField()

    def __str__(self):
        return self.stopName + ' ' + self.subName
