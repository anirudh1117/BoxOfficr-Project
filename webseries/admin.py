from django.contrib import admin
from .models import WebSeries, Season, Episode,WebSeriesCast,WebSeriesRating

@admin.register(WebSeries)
class WebSeriesAdmin(admin.ModelAdmin):
    list_display = ['title', 'release_date']
    list_filter = ['universal_rating']
    search_fields = ['title', 'description']

@admin.register(Season)
class SeasonAdmin(admin.ModelAdmin):
    list_display = ['series', 'season_number', 'title']
    list_filter = ['series', 'universal_rating']
    search_fields = ['title','description']
    autocomplete_fields = ('series',)

@admin.register(Episode)
class EpisodeAdmin(admin.ModelAdmin):
    list_display = ['title', 'season', 'episode_number']
    list_filter = ['season']
    search_fields = ['title', 'synopsis']
    autocomplete_fields = ('season',)

@admin.register(WebSeriesCast)
class WebSeriesCastAdmin(admin.ModelAdmin):
    list_display = ('web_series_worked', 'person', 'role')
    search_fields = ('web_series_worked__title', 'person__first_name', 'person__last_name', 'role')
    autocomplete_fields = ('person', 'web_series_worked',)

@admin.register(WebSeriesRating)
class WebSeriesRatingAdmin(admin.ModelAdmin):
    list_display = ('webSeries', 'agency', 'rating', 'max_rating')
    search_fields = ('webSeries__title', 'agency__name', 'rating', 'max_rating')
