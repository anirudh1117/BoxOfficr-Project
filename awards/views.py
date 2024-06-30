from boxOfficeProject.customPagination import CustomPageNumberPagination
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.http import Http404

from .models import Award, AwardEvent
from .serializer import CelebrityAwardsSerializer, AwardListSerializer, AwardSerializer,AwardEventSerializer
from celebrity.models import Celebrity


class AwardList(APIView):
    permission_classes = []

    def get(self, request, format=None):
        awards = Award.objects.all()
        paginator = CustomPageNumberPagination()
        page = paginator.paginate_queryset(awards, request)

        if page is not None:
            serializer = AwardListSerializer(
                page, many=True, context={"request": request})
            return paginator.get_paginated_response(serializer.data)

        serializer = AwardListSerializer(
            awards, many=True, context={"request": request})
        return Response(serializer.data)
    

class AwardEventsList(APIView):
    permission_classes = []

    def get(self, request, name, format=None):
        awards = Award.objects.filter(name_slug__iexact = name)

        if awards.first():
            serializer = AwardSerializer(
                awards[0], context={"request": request})
            return Response(serializer.data)
        
        return Response([])
    
class AwardEventCategoryList(APIView):
    permission_classes = []

    def get(self, request, name, format=None):
        awards = Award.objects.filter(name_slug__iexact = name)
        awardEvents = awards.events.all().order_by('-year')

        if awardEvents.first():
            serializer = AwardEventSerializer(
                awards[0], context={"request": request})
            return Response(serializer.data)
        
        return Response([])


class CelebrityAwardList(APIView):
    permission_classes = []

    def get(self, request, name, format=None):
        celebrities = Celebrity.objects.filter(
            is_published=True, celebrity_slug__iexact=name)

        if celebrities.first():
            serializer = CelebrityAwardsSerializer(
                celebrities[0],context={"request": request})
            return Response(serializer.data)

        return Response({})
