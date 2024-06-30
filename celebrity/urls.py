from django.urls import path
from .views import CelebritiesList, CelebrityBiographyList, CelebrityFactsAndFAQList

urlpatterns = [
    path('', CelebritiesList.as_view(), name='celebrities-list'),
    path('biography/<str:name>', CelebrityBiographyList.as_view(),
         name='celebrity-biography'),
    path('facts/<str:name>', CelebrityFactsAndFAQList.as_view(),
         name='celebrity-facts')
]
