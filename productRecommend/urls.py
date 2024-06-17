from django.urls import path
from .views import CelebrityProductRecommendList

urlpatterns = [
    path('celebrity/<str:name>',CelebrityProductRecommendList.as_view(),name='celebrity-products'),
]
