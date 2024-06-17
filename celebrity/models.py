from django.db import models

from utils.commonFunction import calculate_next_year, slugify

class FilmIndustry(models.Model):
    name = models.CharField(max_length=100, unique=True)
    name_slug = models.SlugField(blank=True, null=True, editable=False)

    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if self.name:
            self.name_slug = slugify(self.name.upper())
        super().save(*args, **kwargs)


class Role(models.Model):
    name = models.CharField(max_length=100, unique=True)
    name_slug = models.SlugField(blank=True, null=True, editable=False)

    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if self.name:
            self.name_slug = slugify(self.name.upper())
        super().save(*args, **kwargs)

class Celebrity(models.Model):
    
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    image = models.FileField(upload_to='media/celebrities/', null=True, blank=True)
    celebrity_slug = models.SlugField(blank=True, null=True, editable=False)
    description = models.TextField()
    industry = models.ManyToManyField(FilmIndustry, related_name='celebrities_industry')
    roles = models.ManyToManyField(Role, related_name='celebrities_role')
    is_published = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
    
    def save(self, *args, **kwargs):
        if self.first_name:
            fullName = (self.first_name if self.first_name else '') + ' ' + (self.last_name if self.last_name else '')
            self.celebrity_slug = slugify(fullName.upper())
        super().save(*args, **kwargs)

class Biography(models.Model):
    GENDER_CHOICES = [
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Other', 'Other'),
        ('Not Specified', 'Not Specified')
    ]

    MARITAL_STATUS_CHOICES = [
        ('Single', 'Single'),
        ('Married', 'Married'),
        ('Divorced', 'Divorced'),
        ('Widowed', 'Widowed')
    ]

    CURRENCY_CHOICES = [
        ('USD', 'USD'),
        ('INR', 'INR'),
        ('EUR', 'EUR'),
        ('GBP', 'GBP'),
        ('JPY', 'JPY'),
        ('Other', 'Other')
    ]

    ZODIAC_SIGN_CHOICES = [
        ('Aries', 'Aries'),
        ('Taurus', 'Taurus'),
        ('Gemini', 'Gemini'),
        ('Cancer', 'Cancer'),
        ('Leo', 'Leo'),
        ('Virgo', 'Virgo'),
        ('Libra', 'Libra'),
        ('Scorpio', 'Scorpio'),
        ('Sagittarius', 'Sagittarius'),
        ('Capricorn', 'Capricorn'),
        ('Aquarius', 'Aquarius'),
        ('Pisces', 'Pisces')
    ]

    celebrity = models.OneToOneField(Celebrity, on_delete=models.CASCADE, related_name='biography')
    nickname = models.CharField(max_length=100, null=True, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    date_of_death = models.DateField(null=True, blank=True)
    marital_status = models.CharField(max_length=20, choices=MARITAL_STATUS_CHOICES, null=True, blank=True)
    nationality = models.CharField(max_length=100, null=True, blank=True)
    gender = models.CharField(max_length=20, choices=GENDER_CHOICES, default='Not Specified')
    image = models.FileField(upload_to='media/celebrities/', null=True, blank=True)
    net_worth_currency = models.CharField(max_length=10, choices=CURRENCY_CHOICES, null=True, blank=True)
    net_worth = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    #spouse = models.OneToOneField('self', on_delete=models.SET_NULL, null=True, blank=True, related_name='married_to')
    #parents = models.ManyToManyField('self', blank=True, related_name='children', symmetrical=False)
    height = models.CharField(max_length=20, null=True, blank=True)
    eye_color = models.CharField(max_length=50, null=True, blank=True)
    hair_color = models.CharField(max_length=50, null=True, blank=True)
    birthplace = models.CharField(max_length=255, null=True, blank=True)
    zodiac_sign = models.CharField(max_length=50, choices=ZODIAC_SIGN_CHOICES, null=True, blank=True)
    hometown = models.CharField(max_length=255, null=True, blank=True)
    school = models.CharField(max_length=255, null=True, blank=True)
    college = models.CharField(max_length=255, null=True, blank=True)
    education_qualification = models.CharField(max_length=255, null=True, blank=True)
    ethnicity = models.CharField(max_length=100, null=True, blank=True)
    vegetarian = models.BooleanField(default=False)
    favorite_food = models.CharField(max_length=255, null=True, blank=True)
    website = models.URLField(max_length=200, null=True, blank=True)
    instagram_followers = models.IntegerField(null=True, blank=True)
    instagram = models.URLField(max_length=200, null=True, blank=True)
    twitter = models.URLField(max_length=200, null=True, blank=True)
    facebook = models.URLField(max_length=200, null=True, blank=True)
    youtube = models.URLField(max_length=200, null=True, blank=True)

    def __str__(self):
        return f"Biography of {self.celebrity.first_name} {self.celebrity.last_name}"