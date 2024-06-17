from django.urls import path
from .views import CelebritiesList, CelebrityBiographyList

urlpatterns = [
    path('',CelebritiesList.as_view(),name='celebrities-list'),
    path('biography/<str:name>',CelebrityBiographyList.as_view(),name='celebrity-biography'),
]
