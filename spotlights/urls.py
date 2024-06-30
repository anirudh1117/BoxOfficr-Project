from django.urls import path
from .views import SpotlightDataView

urlpatterns = [
    path('', SpotlightDataView.as_view(), name='spotlight-data'),
]
