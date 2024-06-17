from django.urls import path
from .views import CelebrityAwardList, AwardList, AwardEventsList

urlpatterns = [
    path('', AwardList.as_view(), name='awards-list'),
    path('<str:name>', AwardEventsList.as_view(), name='award-event-list'),
    path('celebrity/<str:name>', CelebrityAwardList.as_view(),
         name='celebrity-awards'),
]
