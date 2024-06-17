from django.utils import timezone
from rest_framework.response import Response
from rest_framework.views import APIView

from boxOfficeProject.customPagination import CustomPageNumberPagination
from celebrity.models import Celebrity
from .models import Movie
from .serializer import BoxOfficeSerializer, CelebrityMovieSerializer,MovieShortSerilaizer


class BoxOfficeList(APIView):
    permission_classes = []

    def get(self, request,format=None):
        movies = Movie.objects.all()
        paginator = CustomPageNumberPagination()
        page = paginator.paginate_queryset(movies, request)

        if page is not None:
            serializer = BoxOfficeSerializer(
            page, many=True, context={"request": request})
            return paginator.get_paginated_response(serializer.data)
        
        serializer = BoxOfficeSerializer(movies, many=True, context={"request": request})
        return Response(serializer.data)
    

class UpcomingMovieList(APIView):
    permission_classes = []

    def get(self, request,format=None):
        current_date = timezone.now().date()
        movies = Movie.objects.filter(release_date__gt=current_date)
        paginator = CustomPageNumberPagination()
        page = paginator.paginate_queryset(movies, request)

        if page is not None:
            serializer = MovieShortSerilaizer(
            page, many=True, context={"request": request})
            return paginator.get_paginated_response(serializer.data)
        
        serializer = MovieShortSerilaizer(movies, many=True, context={"request": request})
        return Response(serializer.data)
    
class LatestMovieList(APIView):
    permission_classes = []

    def get(self, request,format=None):
        current_date = timezone.now().date()
        movies = Movie.objects.filter(release_date__lt=current_date).order_by('-release_date')
        paginator = CustomPageNumberPagination()
        page = paginator.paginate_queryset(movies, request)

        if page is not None:
            serializer = MovieShortSerilaizer(
            page, many=True, context={"request": request})
            return paginator.get_paginated_response(serializer.data)
        
        serializer = MovieShortSerilaizer(movies, many=True, context={"request": request})
        return Response(serializer.data)
    
class CelebrityUpcomingMovieList(APIView):
    permission_classes = []

    def get(self, request, name, format=None):
        celebrities = Celebrity.objects.filter(
            is_published=True, celebrity_slug__iexact=name)

        if celebrities.first():
            serializer = CelebrityMovieSerializer(
                celebrities[0],context={"request": request})
            return Response(serializer.data)

        return {}