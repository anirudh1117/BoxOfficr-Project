from django.db import models

from celebrity.models import Celebrity, Role
from movie.models import AvailableMedia, Genre, Language, MovieTags, RatingAgency
from utils.commonFunction import slugify


class WebSeries(models.Model):

    VERDICT_CHOICES = [
        ('Hit', 'Hit'),
        ('Flop', 'Flop'),
        ('Average', 'Average'),
        ('Super Hit', 'Super Hit'),
        ('Blockbuster', 'Blockbuster')
    ]

    RATING_CHOICES = (
        ('G', 'General Audiences – All Ages Admitted'),
        ('PG', 'Parental Guidance Suggested – Some Material May Not Be Suitable for Children'),
        ('PG-13', 'Parents Strongly Cautioned – Some Material May Be Inappropriate for Children Under 13'),
        ('R', 'Restricted – Under 17 Requires Accompanying Parent or Adult Guardian'),
        ('NC-17', 'Adults Only – No One 17 and Under Admitted'),
        ('NR', 'Not Rated'),
    )

    title = models.CharField(max_length=255)
    title_slug = models.SlugField(blank=True, null=True, editable=False)
    description = models.TextField()
    release_date = models.DateField()
    genres = models.ManyToManyField(Genre, related_name='web_series_genres')
    tags = models.ManyToManyField(
        MovieTags, related_name='web_series_tags')
    director = models.ManyToManyField(
        Celebrity, blank=True, related_name='by_directed_web_series')
    producers = models.ManyToManyField(
        Celebrity, related_name='produced_web_series', blank=True)
    official_trailer_url = models.URLField(blank=True, null=True)
    language = language = models.ManyToManyField(
        Language, blank=True)
    plot = models.TextField(null=True, blank=True)
    poster = models.FileField(
        upload_to='media/web-series/posters/', null=True, blank=True)
    trailer_url = models.URLField(max_length=200, null=True, blank=True)
    rotten_tomatoes_score = models.DecimalField(
        max_digits=3, decimal_places=1, null=True, blank=True)
    universal_rating = models.CharField(
        max_length=5, choices=RATING_CHOICES, blank=True, null=True, help_text="Universal content rating")
    verdict = models.CharField(
        max_length=20, choices=VERDICT_CHOICES, null=True, blank=True)
    available_on = models.ManyToManyField(
        AvailableMedia, related_name='web_series')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if self.title:
            self.title_slug = slugify(self.title.upper())
        super().save(*args, **kwargs)


class Season(models.Model):

    VERDICT_CHOICES = [
        ('Hit', 'Hit'),
        ('Flop', 'Flop'),
        ('Average', 'Average'),
        ('Super Hit', 'Super Hit'),
        ('Blockbuster', 'Blockbuster')
    ]

    RATING_CHOICES = (
        ('G', 'General Audiences – All Ages Admitted'),
        ('PG', 'Parental Guidance Suggested – Some Material May Not Be Suitable for Children'),
        ('PG-13', 'Parents Strongly Cautioned – Some Material May Be Inappropriate for Children Under 13'),
        ('R', 'Restricted – Under 17 Requires Accompanying Parent or Adult Guardian'),
        ('NC-17', 'Adults Only – No One 17 and Under Admitted'),
        ('NR', 'Not Rated'),
    )

    series = models.ForeignKey(
        WebSeries, on_delete=models.CASCADE, related_name='seasons')
    title = models.CharField(max_length=255)
    title_slug = models.SlugField(blank=True, null=True, editable=False)
    plot = models.TextField(null=True, blank=True)
    season_number = models.PositiveIntegerField()
    description = models.TextField(blank=True, null=True)
    release_date = models.DateField()
    cast = models.ManyToManyField(
        Celebrity, through='WebSeriesCast', related_name='acted_web_series', blank=True)
    poster = models.ImageField(
        upload_to='media/web-series/seasons/posters/', blank=True, null=True)
    promotional_video_url = models.URLField(blank=True, null=True)
    subtitle_languages = models.ManyToManyField(
        Language, blank=True,related_name="season_subtitle_language",  help_text="Available subtitle languages")
    audio_languages = models.ManyToManyField(
        Language, blank=True,related_name="season_audio_language",  help_text="Available Audio languages")
    universal_rating = models.CharField(
        max_length=5, choices=RATING_CHOICES, blank=True, null=True, help_text="Universal content rating")
    verdict = models.CharField(
        max_length=20, choices=VERDICT_CHOICES, null=True, blank=True)
    available_on = models.ManyToManyField(
        AvailableMedia, related_name='web_series_media')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('series', 'season_number')
        ordering = ['season_number']

    def __str__(self):
        return f"{self.series.title} - Season {self.season_number}"

    def save(self, *args, **kwargs):
        if self.title:
            self.title_slug = slugify(self.title.upper())
        super().save(*args, **kwargs)


class Episode(models.Model):
    season = models.ForeignKey(Season, on_delete=models.CASCADE, related_name='episodes')
    episode_number = models.PositiveIntegerField()
    title = models.CharField(max_length=555)
    title_slug = models.SlugField(blank=True, null=True, editable=False)
    plot = models.TextField(null=True, blank=True)
    poster = models.ImageField(
        upload_to='media/web-series/seasons/episodes/posters/', blank=True, null=True)
    duration = models.IntegerField(help_text="Duration in minutes")
    release_date = models.DateField()
    synopsis = models.TextField(blank=True, null=True)
    video_url = models.URLField(blank=True, null=True)
    has_subtitles = models.BooleanField(default=False)
    subtitle_languages = models.ManyToManyField(
        Language, blank=True, related_name="epidosde_subtitle_language", help_text="Available subtitle languages")
    audio_languages = models.ManyToManyField(
        Language, blank=True, related_name="epdisode_audio_language",  help_text="Available Audio languages")
    view_count = models.PositiveIntegerField(default=0)
    likes = models.PositiveIntegerField(default=0)
    dislikes = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('season', 'episode_number')
        ordering = ['episode_number']

    def __str__(self):
        return f"{self.season.series.title} - S{self.season.season_number}E{self.episode_number} - {self.title}"
    
    def save(self, *args, **kwargs):
        if self.title:
            self.title_slug = slugify(self.title.upper())
        super().save(*args, **kwargs)

class WebSeriesCast(models.Model):
    web_series_worked = models.ForeignKey(
        Season, on_delete=models.CASCADE, related_name='web_series_worked')
    person = models.ForeignKey(Celebrity, on_delete=models.CASCADE)
    role = models.ForeignKey(Role, on_delete=models.DO_NOTHING)

    def __str__(self):
        return f"{self.person.first_name} {self.person.last_name} as {self.role} in {self.web_series_worked.title}"
    
class WebSeriesRating(models.Model):
    webSeries = models.ForeignKey(
        Season, on_delete=models.CASCADE, related_name='web_series_ratings')
    agency = models.ForeignKey(
        RatingAgency, on_delete=models.CASCADE, related_name='web_series_ratings')
    rating = models.DecimalField(max_digits=3, decimal_places=1)
    max_rating = models.IntegerField()
    url = models.URLField(max_length=200, null=True, blank=True)

    def __str__(self):
        return f"{self.webSeries.title} - {self.agency.name} - {self.rating}/{self.max_rating}"



