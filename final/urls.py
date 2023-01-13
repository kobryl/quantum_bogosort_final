from django.urls import path

from . import views

app_name = 'final'
urlpatterns = [
    path('', views.index, name='index'),
    path('trasa/', views.trasa, name='trasa')
]
