from django.db import models

from celebrity.models import Celebrity, Role
from utils.commonFunction import slugify


class Language(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class Genre(models.Model):
    name = models.CharField(max_length=100, unique=True)
    name_slug = models.SlugField(blank=True, null=True, editable=False)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if self.name:
            self.name_slug = slugify(self.name.upper())
        super().save(*args, **kwargs)


class MovieTags(models.Model):
    name = models.CharField(max_length=100, unique=True)
    name_slug = models.SlugField(blank=True, null=True, editable=False)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if self.name:
            self.name_slug = slugify(self.name.upper())
        super().save(*args, **kwargs)


class AvailableMedia(models.Model):
    name = models.CharField(max_length=100, unique=True)
    name_slug = models.SlugField(blank=True, null=True, editable=False)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if self.name:
            self.name_slug = slugify(self.name.upper())
        super().save(*args, **kwargs)


class Movie(models.Model):

    VERDICT_CHOICES = [
        ('Hit', 'Hit'),
        ('Flop', 'Flop'),
        ('Average', 'Average'),
        ('Super Hit', 'Super Hit'),
        ('Blockbuster', 'Blockbuster')
    ]

    CURRENCY_CHOICES = [
        ('USD', 'USD'),
        ('INR', 'INR'),
        ('EUR', 'EUR'),
        ('GBP', 'GBP'),
        ('JPY', 'JPY'),
        ('Other', 'Other')
    ]

    AVAILABLE_ON_CHOICES = [
        ('Theater', 'Theater'),
        ('Prime', 'Prime'),
        ('Netflix', 'Netflix'),
        ('Jio Cinema', 'Jio Cinema'),
        ('Apple TV', 'Apple TV'),
        ('Zee5', 'Zee5'),
        ('Disney Hotstar', 'Disney Hotstar'),
        ('MX Player', 'MX Player'),
        ('Voot', 'Voot')
    ]

    VALUE_UNIT_CHOICES = [
        ('crores', 'Crores'),
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
    release_date = models.DateField()
    duration = models.IntegerField(help_text='Duration in minutes')
    genres = models.ManyToManyField(Genre, related_name='movies')
    tags = models.ManyToManyField(
        MovieTags, related_name='movie_tags', blank=True)
    director = models.ManyToManyField(
        Celebrity, blank=True, related_name='by_directed_movies')
    producers = models.ManyToManyField(
        Celebrity, related_name='produced_movies', blank=True)
    cast = models.ManyToManyField(
        Celebrity, through='Cast', related_name='acted_movies', blank=True)
    plot = models.TextField(null=True, blank=True)
    language = models.ManyToManyField(
        Language, blank=True)
    collection_currency = models.CharField(
        max_length=10, choices=CURRENCY_CHOICES, default='INR')
    budget_currency = models.CharField(
        max_length=10, choices=CURRENCY_CHOICES, null=True, blank=True, default='INR')
    budget = models.DecimalField(
        max_digits=15, decimal_places=2, null=True, blank=True)
    budget_unit = models.CharField(
        max_length=8, choices=VALUE_UNIT_CHOICES, default='crores')
    poster = models.FileField(
        upload_to='media/movies/posters/', null=True, blank=True)
    trailer_url = models.URLField(max_length=200, null=True, blank=True)
    rotten_tomatoes_score = models.DecimalField(
        max_digits=3, decimal_places=1, null=True, blank=True)
    universal_rating = models.CharField(
        max_length=5, choices=RATING_CHOICES, blank=True, null=True, help_text="Universal content rating")
    verdict = models.CharField(
        max_length=20, choices=VERDICT_CHOICES, null=True, blank=True)
    available_on = models.ManyToManyField(
        AvailableMedia, related_name='movies')
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if self.title:
            self.title_slug = slugify(self.title.upper())
        super().save(*args, **kwargs)

    def total_box_office_collection(self):
        total_collection = self.box_office_figures.aggregate(
            total=models.Sum('collection')
        )['total'] or 0
        return total_collection


class Cast(models.Model):
    movie_worked = models.ForeignKey(
        Movie, on_delete=models.CASCADE, related_name='movie_worked')
    person = models.ForeignKey(Celebrity, on_delete=models.CASCADE)
    role = models.ForeignKey(Role, on_delete=models.DO_NOTHING)

    def __str__(self):
        return f"{self.person.first_name} {self.person.last_name} as {self.role} in {self.movie_worked.title}"


class BoxOffice(models.Model):
    COUNTRY_CHOICES = [
        ('India', 'India'),
        ('USA', 'USA'),
        ('UK', 'UK'),
        ('China', 'China'),
        ('Worldwide', 'Worldwide')
    ]

    CURRENCY_CHOICES = [
        ('USD', 'USD'),
        ('INR', 'INR'),
        ('EUR', 'EUR'),
        ('GBP', 'GBP'),
        ('JPY', 'JPY'),
        ('Other', 'Other')
    ]

    DAY_CHOICES = [
        ('day1', 'Day 1'),
        ('day2', 'Day 2'),
        ('day3', 'Day 3'),
        ('day4', 'Day 4'),
        ('day5', 'Day 5'),
        ('day6', 'Day 6'),
        ('day7', 'Day 7'),
        ('day8', 'Day 8'),
        ('day9', 'Day 9'),
        ('day10', 'Day 10'),
        ('day11', 'Day 11'),
        ('day12', 'Day 12'),
        ('day13', 'Day 13'),
        ('day14', 'Day 14'),
        ('day15', 'Day 15'),
    ]

    VALUE_UNIT_CHOICES = [
        ('crores', 'Crores'),
    ]

    movie = models.ForeignKey(
        Movie, on_delete=models.CASCADE, related_name='box_office_figures')
    date = models.DateField(null=True)
    day = models.CharField(max_length=5, choices=DAY_CHOICES, null=True)
    country = models.CharField(max_length=20, choices=COUNTRY_CHOICES)
    collection = models.DecimalField(max_digits=15, decimal_places=2)
    value_unit = models.CharField(
        max_length=8, choices=VALUE_UNIT_CHOICES, default='crores')

    def __str__(self):
        return f"{self.movie.title} - {self.day} - {self.collection} {self.value_unit} - {self.country}"


class RatingAgency(models.Model):
    name = models.CharField(max_length=100, unique=True)
    website = models.URLField(max_length=200, null=True, blank=True)

    def __str__(self):
        return self.name


class Rating(models.Model):
    movie = models.ForeignKey(
        Movie, on_delete=models.CASCADE, related_name='ratings')
    agency = models.ForeignKey(
        RatingAgency, on_delete=models.CASCADE, related_name='ratings')
    rating = models.DecimalField(max_digits=3, decimal_places=1)
    max_rating = models.IntegerField()
    url = models.URLField(max_length=200, null=True, blank=True)

    def __str__(self):
        return f"{self.movie.title} - {self.agency.name} - {self.rating}/{self.max_rating}"
