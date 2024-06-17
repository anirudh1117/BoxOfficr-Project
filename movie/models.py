from django.db import models

from celebrity.models import Celebrity, Role
from utils.commonFunction import slugify


class Genre(models.Model):
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

    title = models.CharField(max_length=255)
    title_slug = models.SlugField(blank=True, null=True, editable=False)
    release_date = models.DateField()
    duration = models.IntegerField(help_text='Duration in minutes')
    genres = models.ManyToManyField(Genre, related_name='movies')
    director = models.ManyToManyField(Celebrity, blank=True, related_name='by_directed_movies')
    producers = models.ManyToManyField(Celebrity, related_name='produced_movies', blank=True)
    cast = models.ManyToManyField(Celebrity, through='Cast', related_name='acted_movies', blank=True)
    plot = models.TextField(null=True, blank=True)
    language = models.CharField(max_length=100, null=True, blank=True)
    budget_currency = models.CharField(max_length=10, choices=CURRENCY_CHOICES, null=True, blank=True)
    budget = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    poster = models.FileField(upload_to='movies/posters/', null=True, blank=True)
    trailer_url = models.URLField(max_length=200, null=True, blank=True)
    rotten_tomatoes_score = models.DecimalField(max_digits=3, decimal_places=1, null=True, blank=True)
    verdict = models.CharField(max_length=20, choices=VERDICT_CHOICES, null=True, blank=True)
    available_on = models.CharField(max_length=20, choices=AVAILABLE_ON_CHOICES, null=True, blank=True)

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
    movie_worked = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='movie_worked')
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

    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='box_office_figures')
    date = models.DateField()
    country = models.CharField(max_length=20, choices=COUNTRY_CHOICES)
    collection_currency = models.CharField(max_length=10, choices=CURRENCY_CHOICES, null=True, blank=True)
    collection = models.DecimalField(max_digits=15, decimal_places=2)

    def __str__(self):
        return f"{self.movie.title} - {self.date} - {self.country}"
    

class RatingAgency(models.Model):
    name = models.CharField(max_length=100, unique=True)
    website = models.URLField(max_length=200, null=True, blank=True)

    def __str__(self):
        return self.name
    
class Rating(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='ratings')
    agency = models.ForeignKey(RatingAgency, on_delete=models.CASCADE, related_name='ratings')
    rating = models.DecimalField(max_digits=3, decimal_places=1)
    max_rating = models.IntegerField()
    url = models.URLField(max_length=200, null=True, blank=True)

    def __str__(self):
        return f"{self.movie.title} - {self.agency.name} - {self.rating}/{self.max_rating}"


