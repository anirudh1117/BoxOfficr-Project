from django.urls import path
from .views import UpcomingSeasonsView

urlpatterns = [
    path('upcoming', UpcomingSeasonsView.as_view(), name='upcoming-web-series'),
]
