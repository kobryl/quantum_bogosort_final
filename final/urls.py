from django.urls import path

from . import views

app_name = 'final'
urlpatterns = [
    path('', views.index, name='index'),
    path('create_path/', views.create_path, name='create_path')
]
