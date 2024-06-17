from rest_framework import serializers
from django.db import models
from django.utils import timezone
from django.db.models import Q

from celebrity.serializer import CelebrityNameAndSlugSerializer, FilmIndustrySerializer, RoleSerializer
from utils.commonFunction import convert_budget

from .models import Movie, BoxOffice
from celebrity.models import Celebrity


class BoxOfficeSerializer(serializers.ModelSerializer):
    poster = serializers.SerializerMethodField()
    movie_budget = serializers.SerializerMethodField()
    box_office_collection = serializers.SerializerMethodField()
    genres = serializers.SerializerMethodField()

    def get_poster(self, movieObj):
        request = self.context.get("request")
        image_url = ''
        if movieObj.poster:
            image_url = movieObj.poster.url
        else:
            pass
        path = request.build_absolute_uri()
        path = path.replace('//', '/')
        path = path.split('/')
        url = path[0] + "//" + path[1] + image_url
        return url

    def get_movie_budget(self, movieObj):
        budget = movieObj.budget
        converted_budget = convert_budget(budget)
        return converted_budget + movieObj.budget_currency

    def get_box_office_collection(self, movieObj):
        total_collection = self.total_box_office_collection(movieObj)
        converted_collection = convert_budget(total_collection)
        return str(converted_collection) + ' INR'

    def get_genres(self, obj):
        return ", ".join([genre.name for genre in obj.genres.all()])

    def total_box_office_collection(self, movieObj):
        total_collection = movieObj.box_office_figures.aggregate(
            total=models.Sum('collection')
        )['total'] or 0
        return total_collection

    class Meta:
        model = Movie
        fields = ('title', 'movie_budget', 'box_office_collection',
                  'verdict', 'poster', 'genres')


class MovieTitleAndSlugSerializer(serializers.ModelSerializer):

    class Meta:
        model = Movie
        fields = ('title', 'title_slug')


class MovieShortSerilaizer(serializers.ModelSerializer):
    poster = serializers.SerializerMethodField()
    genres = serializers.SerializerMethodField()
    duration = serializers.SerializerMethodField()
    cast = serializers.SerializerMethodField()
    similar_movies = serializers.SerializerMethodField()

    def get_duration(self, movieObj):
        if movieObj is not None and movieObj.duration:
            return str(movieObj.duration) + " minutes"

        return "- minutes"

    def get_poster(self, movieObj):
        request = self.context.get("request")
        image_url = ''
        if movieObj.poster:
            image_url = movieObj.poster.url
        else:
            pass
        path = request.build_absolute_uri()
        path = path.replace('//', '/')
        path = path.split('/')
        url = path[0] + "//" + path[1] + image_url
        return url

    def get_genres(self, obj):
        return ", ".join([genre.name for genre in obj.genres.all()])

    def get_cast(self, movieObj):
        cast = movieObj.cast.all() if movieObj.cast else []
        celebrities = Celebrity.objects.filter(id__in=cast)
        if celebrities.first():
            serializer = CelebrityNameAndSlugSerializer(
                celebrities, many=True,  context=self.context)
            return serializer.data

        return []

    def get_similar_movies(self, movie):
        similar_movies = Movie.objects.filter(
            Q(genres__in=movie.genres.all()) &
            ~Q(id=movie.id)
        ).distinct().order_by('-release_date')[:3]

        if similar_movies.first():
            serializer = MovieTitleAndSlugSerializer(
                similar_movies, many=True,  context=self.context)
            return serializer.data

        return []

    class Meta:
        model = Movie
        fields = ('title', 'verdict', 'poster',
                  'genres', 'release_date', 'title_slug', 'language', 'cast', 'duration', 'plot', 'trailer_url', 'similar_movies', 'available_on')


class CelebrityMovieSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()
    industry = FilmIndustrySerializer(many=True)
    roles = RoleSerializer(many=True)
    upcoming_movies = serializers.SerializerMethodField()

    def get_image(self, celebrity):
        request = self.context.get("request")
        image_url = ''
        if celebrity.image:
            image_url = celebrity.image.url
        else:
            pass
        path = request.build_absolute_uri()
        path = path.replace('//', '/')
        path = path.split('/')
        url = path[0] + "//" + path[1] + image_url
        return url

    def get_upcoming_movies(self, celebrity):
        current_date = timezone.now().date()

        movies = Movie.objects.filter(
            release_date__gt=current_date,
            cast=celebrity
        ).distinct()

        if movies.first():
            serializer = MovieShortSerilaizer(
                movies, many=True,  context=self.context)
            return serializer.data

        return []

    class Meta:
        model = Celebrity
        fields = '__all__'
