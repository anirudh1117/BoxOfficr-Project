from rest_framework import serializers
from django.db import models
from django.utils import timezone
from django.db.models import Q
from django.db.models import Sum

from celebrity.serializer import CelebrityNameAndSlugSerializer, CelebrityTagsSerializer, FilmIndustrySerializer, RoleSerializer
from utils.commonFunction import convert_budget, crore_to_million

from .models import Movie, BoxOffice
from celebrity.models import Celebrity


class BoxOfficeSerializer(serializers.ModelSerializer):
    poster = serializers.SerializerMethodField()
    movie_budget_in_crores = serializers.SerializerMethodField()
    movie_budget_in_millions = serializers.SerializerMethodField()
    box_office_collection_in_crores = serializers.SerializerMethodField()
    box_office_collection_in_millions = serializers.SerializerMethodField()
    day1_box_office_collection = serializers.SerializerMethodField()
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

    def get_movie_budget_in_crores(self, movieObj):
        if movieObj.budget:
            return f"{movieObj.budget:.2f} Crores"
        return "Budget NA"

    def get_movie_budget_in_millions(self, movieObj):
        if movieObj.budget:
            return f"{crore_to_million(movieObj.budget):.2f} Million"
        return "Budget NA"

    def get_box_office_collection_in_crores(self, movieObj):
        total_collection_inr = movieObj.box_office_figures.aggregate(
            total=Sum('collection'))['total'] or 0
        return f"{total_collection_inr:.2f} Crores"

    def get_box_office_collection_in_millions(self, movieObj):
        total_collection_inr = movieObj.box_office_figures.aggregate(
            total=Sum('collection'))['total'] or 0
        return f"{crore_to_million(total_collection_inr):.2f} Million"

    def get_day1_box_office_collection(self, movieObj):
        day1_entries = movieObj.box_office_figures.filter(
            day='day1').aggregate(total=Sum('collection'))['total'] or 0
        return f"{day1_entries:.2f} Crores"

    def get_genres(self, obj):
        return ", ".join([genre.name for genre in obj.genres.all()])

    def total_box_office_collection(self, movieObj):
        total_collection = movieObj.box_office_figures.aggregate(
            total=models.Sum('collection')
        )['total'] or 0
        return total_collection

    class Meta:
        model = Movie
        fields = (
            'title', 'movie_budget_in_crores', 'movie_budget_in_millions', 'box_office_collection_in_crores', 'box_office_collection_in_millions',
            'day1_box_office_collection', 'verdict', 'poster', 'genres', 'collection_currency', 'budget_currency', 'title_slug', 'release_date'
        )


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
    available_on = serializers.SerializerMethodField()
    language = serializers.SerializerMethodField()

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

    def get_available_on(self, obj):
        return ", ".join([media.name for media in obj.available_on.all()])

    def get_language(self, obj):
        return ", ".join([language.name for language in obj.language.all()])

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
    tags = CelebrityTagsSerializer(many=True)
    upcoming_movies = serializers.SerializerMethodField()
    author = serializers.SerializerMethodField()
    upcoming_movies_count = serializers.SerializerMethodField()
    recommended_products_count = serializers.SerializerMethodField()
    awards_count = serializers.SerializerMethodField()
    vehicle_collection_count = serializers.SerializerMethodField()

    def get_upcoming_movies_count(self, celebrity):
        current_date = timezone.now().date()
        return Movie.objects.filter(movie_worked__person=celebrity, release_date__gte=current_date).count()

    def get_recommended_products_count(self, celebrity):
        return celebrity.product_recommendations.count()

    def get_awards_count(self, celebrity):
        return celebrity.nominations.filter(winner=True).count()

    def get_vehicle_collection_count(self, celebrity):
        return celebrity.vehicle_ownerships.count()

    def get_author(self, celebrity):
        if celebrity.author:
            full_name = (celebrity.author.first_name if celebrity.author.first_name else '') + \
                ' ' + (celebrity.author.last_name if celebrity.author.last_name else '')
            return full_name
        return "Admin"

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


class MovieNameAndSlugSerializer(serializers.ModelSerializer):

    class Meta:
        model = Movie
        fields = ('title', 'title_slug')
