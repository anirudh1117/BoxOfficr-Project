from django.contrib import admin
from .models import Movie, Genre, Cast, BoxOffice, RatingAgency, Rating

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
    list_display = ('title', 'release_date', 'duration', 'rotten_tomatoes_score', 'verdict')
    search_fields = ('title', 'director__first_name', 'director__last_name')
    filter_horizontal = ('genres', 'producers')

@admin.register(BoxOffice)
class BoxOfficeAdmin(admin.ModelAdmin):
    list_display = ('movie', 'date', 'country', 'collection')
    search_fields = ('movie__title', 'date', 'country')

@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    list_display = ('movie', 'agency', 'rating', 'max_rating')
    search_fields = ('movie__title', 'agency__name', 'rating', 'max_rating')

@admin.register(Cast)
class CastAdmin(admin.ModelAdmin):
    list_display = ('movie_worked', 'person', 'role')
    search_fields = ('movie_worked__title', 'person__first_name', 'person__last_name', 'role')
