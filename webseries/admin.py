from django.contrib import admin
from .models import WebSeries, Season, Episode, WebSeriesCast, WebSeriesRating


@admin.register(WebSeries)
class WebSeriesAdmin(admin.ModelAdmin):
    list_display = ('title', 'release_date', 'verdict', 'created_at')
    search_fields = ('title', 'description', 'plot')
    list_filter = ('release_date', 'verdict', 'genres', 'tags',
                   'language', 'universal_rating', 'available_on')
    filter_horizontal = ('genres', 'tags', 'director',
                         'producers', 'language', 'available_on')


@admin.register(Season)
class SeasonAdmin(admin.ModelAdmin):
    list_display = ('series', 'season_number', 'title',
                    'release_date', 'verdict', 'created_at')
    search_fields = ('series__title', 'title', 'plot')
    list_filter = ('series__title', 'cast', 'verdict', 'release_date',
                   'universal_rating', 'available_on')


@admin.register(Episode)
class EpisodeAdmin(admin.ModelAdmin):
    list_display = ('season', 'episode_number', 'title',
                    'release_date', 'duration', 'view_count', 'likes', 'dislikes')
    search_fields = ('season__series__title', 'season__title', 'title', 'plot')
    list_filter = ('season__series__title', 'season',
                   'release_date', 'has_subtitles')


@admin.register(WebSeriesCast)
class WebSeriesCastAdmin(admin.ModelAdmin):
    list_display = ('web_series_worked', 'person', 'role', 'character_name')
    search_fields = ('web_series_worked__title',
                     'person__first_name', 'person__last_name', 'role')
    autocomplete_fields = ('person', 'web_series_worked',)
    list_filter = ('web_series_worked__series__title', 'role')


@admin.register(WebSeriesRating)
class WebSeriesRatingAdmin(admin.ModelAdmin):
    list_display = ('webSeries', 'agency', 'rating', 'max_rating')
    search_fields = ('webSeries__title', 'agency__name',
                     'rating', 'max_rating')
    list_filter = ('webSeries__series__title', 'agency__name', 'rating')
