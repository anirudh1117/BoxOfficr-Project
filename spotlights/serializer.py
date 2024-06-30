from rest_framework import serializers

from celebrity.serializer import CelebrityNameAndSlugSerializer
from movie.serializer import MovieNameAndSlugSerializer
from webseries.serializers import WebSeriesNameAndSlugSerializer
from .models import SpotlightCelebrities, SpotlightMovies,SpotlightWebSeries


class SpotlightCelebritySerializer(serializers.ModelSerializer):
    celebrity = CelebrityNameAndSlugSerializer(many=True)
    author = serializers.SerializerMethodField()

    def get_author(self, celebrity):
        if celebrity.author:
            full_name = (celebrity.author.first_name if celebrity.author.first_name else '') + \
                ' ' + (celebrity.author.last_name if celebrity.author.last_name else '')
            return full_name
        return "Admin"

    class Meta:
        model = SpotlightCelebrities
        fields = ['celebrity', 'heading', 'description',
                  'created_at', 'updated_at', 'author']


class SpotlightMovieSerializer(serializers.ModelSerializer):
    movies = MovieNameAndSlugSerializer(many=True)
    author = serializers.SerializerMethodField()

    def get_author(self, celebrity):
        if celebrity.author:
            full_name = (celebrity.author.first_name if celebrity.author.first_name else '') + \
                ' ' + (celebrity.author.last_name if celebrity.author.last_name else '')
            return full_name
        return "Admin"

    class Meta:
        model = SpotlightMovies
        fields = ['movies', 'heading', 'description',
                  'created_at', 'updated_at','author']
        

class SpotlightWebSeriesSerializer(serializers.ModelSerializer):
    web_series = WebSeriesNameAndSlugSerializer(many=True)
    author = serializers.SerializerMethodField()

    def get_author(self, celebrity):
        if celebrity.author:
            full_name = (celebrity.author.first_name if celebrity.author.first_name else '') + \
                ' ' + (celebrity.author.last_name if celebrity.author.last_name else '')
            return full_name
        return "Admin"

    class Meta:
        model = SpotlightWebSeries
        fields = ['web_series', 'heading', 'description',
                  'created_at', 'updated_at','author']
