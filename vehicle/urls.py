from django.urls import path
from .views import CelebrityVehicleList

urlpatterns = [
    path('celebrity/<str:name>',CelebrityVehicleList.as_view(),name='celebrity-vehicle'),
]
