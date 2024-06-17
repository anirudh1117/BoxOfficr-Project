from django.urls import path
from .views import BoxOfficeList, UpcomingMovieList, LatestMovieList, CelebrityUpcomingMovieList

urlpatterns = [
    path('box-office', BoxOfficeList.as_view(), name='box-office-list'),
    path('upcoming', UpcomingMovieList.as_view(), name='upcomimg-movie-list'),
    path('latest', LatestMovieList.as_view(), name='latest-movie-list'),
    path('upcoming/<str:name>', CelebrityUpcomingMovieList.as_view(),
         name='celebrity-upcoming-movie'),
]
