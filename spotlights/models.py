from django.db import models
from django.contrib.auth.models import User

from celebrity.models import Celebrity
from movie.models import Movie
from webseries.models import WebSeries


class SpotlightCelebrities(models.Model):
    celebrity = models.ManyToManyField(Celebrity, related_name='spotlight_celebrities')
    heading = models.TextField(blank=True, null=True, help_text="Optional Heading")
    description = models.TextField(blank=True, null=True, help_text="Optional description or highlight text.")
    active = models.BooleanField(default=True, help_text="Toggle visibility")
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

    class Meta:
        verbose_name = "Spotlight Celebrity"
        verbose_name_plural = "Spotlight Celebrities"

    def __str__(self):
        return f"{self.heading} (Spotlight)"
    

class SpotlightMovies(models.Model):
    movies = models.ManyToManyField(Movie, related_name='spotlight_movies')
    heading = models.TextField(blank=True, null=True, help_text="Optional Heading")
    description = models.TextField(blank=True, null=True, help_text="Optional description or highlight text.")
    active = models.BooleanField(default=True, help_text="Toggle visibility")
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

    class Meta:
        verbose_name = "Spotlight Movie"
        verbose_name_plural = "Spotlight Movies"

    def __str__(self):
        return f"{self.heading} (Spotlight)"
    

class SpotlightWebSeries(models.Model):
    web_series = models.ManyToManyField(WebSeries, related_name='spotlight_movies')
    heading = models.TextField(blank=True, null=True, help_text="Optional Heading")
    description = models.TextField(blank=True, null=True, help_text="Optional description or highlight text.")
    active = models.BooleanField(default=True, help_text="Toggle visibility")
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

    class Meta:
        verbose_name = "Spotlight Web Series"
        verbose_name_plural = "Spotlight Web Series"

    def __str__(self):
        return f"{self.heading} (Spotlight)"

