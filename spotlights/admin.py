from django.contrib import admin

from .models import SpotlightCelebrities,SpotlightMovies,SpotlightWebSeries


@admin.register(SpotlightCelebrities)
class SpotlightCelebritiesAdmin(admin.ModelAdmin):
    list_display = ['heading', 'active']
    list_filter = ['active','celebrity']
    list_editable = ['active']
    search_fields = ['celebrity']
    autocomplete_fields = ['celebrity']


@admin.register(SpotlightMovies)
class SpotlightCelebritiesAdmin(admin.ModelAdmin):
    list_display = ['heading', 'active']
    list_filter = ['active','movies']
    list_editable = ['active']
    search_fields = ['movies']
    autocomplete_fields = ['movies']

@admin.register(SpotlightWebSeries)
class SpotlightCelebritiesAdmin(admin.ModelAdmin):
    list_display = ['heading', 'active']
    list_filter = ['active','web_series']
    list_editable = ['active']
    search_fields = ['web_series']
    autocomplete_fields = ['web_series']
