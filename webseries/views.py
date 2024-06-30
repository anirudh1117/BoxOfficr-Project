from django.utils import timezone
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Season
from .serializers import SeasonSerializer


class UpcomingSeasonsView(APIView):
    def get(self, request, *args, **kwargs):
        today = timezone.now().date()
        upcoming_seasons = Season.objects.filter(
            release_date__gt=today).order_by('release_date')
        serializer = SeasonSerializer(
            upcoming_seasons, many=True, context={"request": request})
        return Response(serializer.data)
