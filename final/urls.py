from django.urls import path

from . import views

app_name = 'polls'
urlpatterns = [
    path('', views.index, name='index'),
    path('tf/<int:tf_id>/', views.tf, name='tf'),
]
