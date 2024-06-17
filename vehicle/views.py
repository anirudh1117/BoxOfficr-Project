from boxOfficeProject.customPagination import CustomPageNumberPagination
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.http import Http404

from .serializer import CelebrityVechicleSerializer
from celebrity.models import Celebrity

class CelebrityVehicleList(APIView):
    permission_classes = []

    def get(self, request, name,format=None):
        celebrities = Celebrity.objects.filter(is_published=True, celebrity_slug__iexact = name)

        if celebrities.first():
            serializer = CelebrityVechicleSerializer(
            celebrities[0], context={"request": request})
            return Response(serializer.data)
        
        return {}