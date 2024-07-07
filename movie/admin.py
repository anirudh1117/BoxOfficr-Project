from django.contrib import admin
from .models import Movie, Genre, Cast, BoxOffice, RatingAgency, Rating, AvailableMedia, Language, MovieTags


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


@admin.register(RatingAgency)
class RatingAgencyAdmin(admin.ModelAdmin):
    list_display = ('name', 'website')
    search_fields = ('name', 'website')


@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = ('title', 'release_date',
                    'duration', 'verdict', 'created_at')
    search_fields = ('title', 'plot')
    list_filter = ('release_date', 'verdict', 'genres',
                   'available_on', 'cast', 'tags', 'universal_rating')
    filter_horizontal = ('genres', 'tags', 'director',
                         'producers', 'language', 'available_on')


@admin.register(BoxOffice)
class BoxOfficeAdmin(admin.ModelAdmin):
    list_display = ('movie', 'date', 'day', 'country', 'collection')
    search_fields = ('movie__title', 'date', 'country')
    list_filter = ('country', 'date', 'movie__title', 'day')


@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    list_display = ('movie', 'agency', 'rating', 'max_rating')
    search_fields = ('movie__title', 'agency__name', 'rating', 'max_rating')
    list_filter = ('movie__title', 'agency', 'rating')


@admin.register(Cast)
class CastAdmin(admin.ModelAdmin):
    list_display = ('movie_worked', 'person', 'role', 'character_name')
    search_fields = ('person__first_name',
                     'person__last_name', 'movie_worked__title')
    list_filter = ('movie_worked__title', 'role__name', 'person',)
    autocomplete_fields = ('person', 'movie_worked',)


@admin.register(MovieTags)
class MovieTagsAdmin(admin.ModelAdmin):
    list_display = ('name', 'name_slug')
    search_fields = ('name',)


@admin.register(AvailableMedia)
class AvailableMediaAdmin(admin.ModelAdmin):
    list_display = ('name', 'name_slug')
    search_fields = ('name',)


@admin.register(Language)
class LanguageAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
