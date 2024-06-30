from rest_framework import serializers
from django.db.models import Q

from celebrity.models import Celebrity
from celebrity.serializer import CelebrityNameAndSlugSerializer
from .models import Season, WebSeries


class WebSeriesNameAndSlugSerializer(serializers.ModelSerializer):

    class Meta:
        model = WebSeries
        fields = ('title', 'title_slug')


class SeasonSerializer(serializers.ModelSerializer):
    web_series_title = serializers.SerializerMethodField()
    poster = serializers.SerializerMethodField()
    genres = serializers.SerializerMethodField()
    cast = serializers.SerializerMethodField()
    similar_web_series = serializers.SerializerMethodField()
    available_on = serializers.SerializerMethodField()
    subtitle_languages = serializers.SerializerMethodField()
    audio_languages = serializers.SerializerMethodField()

    def get_web_series_title(self,obj):
        if obj.series and obj.series.title:
            return obj.series.title
        
        return "NA"

    def get_poster(self, seasonObj):
        request = self.context.get("request")
        image_url = ''
        if seasonObj.poster:
            image_url = seasonObj.poster.url
        else:
            pass
        path = request.build_absolute_uri()
        path = path.replace('//', '/')
        path = path.split('/')
        url = path[0] + "//" + path[1] + image_url
        return url

    def get_genres(self, obj):
        return ", ".join([genre.name for genre in obj.series.genres.all()])

    def get_available_on(self, obj):
        return ", ".join([media.name for media in obj.available_on.all()])

    def get_subtitle_languages(self, obj):
        return ", ".join([language.name for language in obj.subtitle_languages.all()])

    def get_audio_languages(self, obj):
        return ", ".join([language.name for language in obj.audio_languages.all()])

    def get_cast(self, obj):
        cast = obj.cast.all() if obj.cast else []
        celebrities = Celebrity.objects.filter(id__in=cast)
        if celebrities.first():
            serializer = CelebrityNameAndSlugSerializer(
                celebrities, many=True,  context=self.context)
            return serializer.data

        return []

    def get_similar_web_series(self, obj):
        similar_web_series = WebSeries.objects.filter(
            Q(genres__in=obj.series.genres.all()) &
            ~Q(id=obj.series.id)
        ).distinct().order_by('-release_date')[:3]

        if similar_web_series.first():
            serializer = WebSeriesNameAndSlugSerializer(
                similar_web_series, many=True,  context=self.context)
            return serializer.data

        return []

    class Meta:
        model = Season
        fields = ('web_series_title', 'title', 'verdict', 'poster',
                  'genres', 'release_date', 'title_slug', 'audio_languages', 'subtitle_languages', 'cast', 'plot', 'promotional_video_url', 'similar_web_series', 'available_on', 'universal_rating')
