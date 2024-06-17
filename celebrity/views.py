from boxOfficeProject.customPagination import CustomPageNumberPagination
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.http import Http404

from .models import Celebrity
from .serializer import CelebritySerializer, CelebrityBiographySerializer

class CelebritiesList(APIView):
    permission_classes = []

    def get(self, request, format=None):
        celebrities = Celebrity.objects.filter(is_published=True)
        paginator = CustomPageNumberPagination()
        page = paginator.paginate_queryset(celebrities, request)

        if page is not None:
            serializer = CelebritySerializer(
            page, many=True, context={"request": request})
            return paginator.get_paginated_response(serializer.data)
        
        serializer = CelebritySerializer(celebrities, many=True, context={"request": request})
        return Response(serializer.data)
    

class CelebrityBiographyList(APIView):
    permission_classes = []

    def get(self, request, name,format=None):
        celebrities = Celebrity.objects.filter(is_published=True, celebrity_slug__iexact = name)

        if celebrities.first():
            serializer = CelebrityBiographySerializer(
            celebrities[0], context={"request": request})
            return Response(serializer.data)
        
        return {}