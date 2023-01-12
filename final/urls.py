from django.urls import path

from . import views

app_name = 'final'
urlpatterns = [
    path('', views.index, name='index'),
    path('tf/<int:tf_id>/', views.tf, name='tf'),
    path('trasa/', views.trasa, name='trasa'),
]
