from django.db import models

from utils.commonFunction import calculate_next_year, slugify
from celebrity.models import Celebrity
from movie.models import Movie


class Award(models.Model):

    COUNTRY_CHOICES = [
        ('India', 'India'),
        ('USA', 'USA'),
        ('UK', 'UK'),
        ('China', 'China'),
        ('Worldwide', 'Worldwide')
    ]

    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(null=True, blank=True)
    image = models.FileField(upload_to='media/awards/', null=True, blank=True)
    name_slug = models.SlugField(blank=True, null=True, editable=False)
    awarded_for = models.CharField(max_length=500, blank=True)
    country = models.CharField(
        max_length=20, choices=COUNTRY_CHOICES, default='India')
    presented_by = models.CharField(max_length=500, blank=True)
    website = models.URLField(max_length=200, null=True, blank=True)
    first_awarded = models.CharField(max_length=500, blank=True)
    last_awarded = models.CharField(max_length=500, blank=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if self.name:
            self.name_slug = slugify(self.name.upper())
        super().save(*args, **kwargs)


class AwardCategory(models.Model):
    award = models.ForeignKey(
        Award, on_delete=models.CASCADE, related_name='categories')
    name = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    name_slug = models.SlugField(blank=True, null=True, editable=False)

    class Meta:
        unique_together = ('award', 'name')

    def __str__(self):
        return f"{self.award.name} - {self.name}"

    def save(self, *args, **kwargs):
        if self.name:
            self.name_slug = slugify(self.name.upper())
        super().save(*args, **kwargs)


class AwardEvent(models.Model):
    YEAR_CHOICES = [(year, year)
                    for year in range(2000, calculate_next_year())]

    award = models.ForeignKey(
        Award, on_delete=models.CASCADE, related_name='events')
    title = models.CharField(max_length=1000, blank=True)
    year = models.IntegerField(choices=YEAR_CHOICES)
    location = models.CharField(max_length=500, blank=True)
    title_slug = models.SlugField(blank=True, null=True, editable=False)
    poster = models.FileField(upload_to='media/awards/', null=True, blank=True)

    class Meta:
        unique_together = ('award', 'year')

    def __str__(self):
        return f"{self.award.name} ({self.year})"

    def save(self, *args, **kwargs):
        if self.title:
            self.title_slug = slugify(self.title.upper())
        super().save(*args, **kwargs)


class Nomination(models.Model):
    category = models.ForeignKey(
        AwardCategory, on_delete=models.CASCADE, related_name='nominations')
    event = models.ForeignKey(
        AwardEvent, on_delete=models.CASCADE, related_name='nominations')
    person = models.ForeignKey(Celebrity, on_delete=models.SET_NULL,
                               null=True, blank=True, related_name='nominations')
    movie = models.ForeignKey(
        Movie, on_delete=models.CASCADE, related_name='nominations')
    winner = models.BooleanField(default=False)

    class Meta:
        unique_together = ('category', 'event', 'person', 'movie')

    def __str__(self):
        nominee = self.person if self.person else self.movie
        return f"{self.event.award.name} - {self.category.name} ({self.event.year}) - {nominee}"
