from django.db import models
from django.contrib.auth.models import User

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


class CelebrityTags(models.Model):
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
    image = models.FileField(
        upload_to='media/celebrities/', null=True, blank=True)
    celebrity_slug = models.SlugField(blank=True, null=True, editable=False)
    description = models.TextField()
    industry = models.ManyToManyField(
        FilmIndustry, related_name='celebrities_industry')
    roles = models.ManyToManyField(Role, related_name='celebrities_role')
    tags = models.ManyToManyField(
        CelebrityTags, related_name='celebrities_tags', blank=True)
    is_published = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    def save(self, *args, **kwargs):
        if self.first_name:
            fullName = (self.first_name if self.first_name else '') + \
                ' ' + (self.last_name if self.last_name else '')
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

    VALUE_UNIT_CHOICES = [
        ('crores', 'Crores'),
    ]

    FOLLOWERS_UNIT_CHOICES = [
        ('million', 'Million'),
    ]

    celebrity = models.OneToOneField(
        Celebrity, on_delete=models.CASCADE, related_name='biography')
    nickname = models.CharField(max_length=100, null=True, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    date_of_death = models.DateField(null=True, blank=True)
    marital_status = models.CharField(
        max_length=20, choices=MARITAL_STATUS_CHOICES, null=True, blank=True)
    nationality = models.CharField(max_length=100, null=True, blank=True)
    gender = models.CharField(
        max_length=20, choices=GENDER_CHOICES, default='Not Specified')
    image = models.FileField(
        upload_to='media/celebrities/', null=True, blank=True)
    net_worth_currency = models.CharField(
        max_length=10, choices=CURRENCY_CHOICES, null=True, blank=True)
    net_worth = models.DecimalField(
        max_digits=15, decimal_places=2, null=True, blank=True)
    worth_value_unit = models.CharField(
        max_length=8, choices=VALUE_UNIT_CHOICES, default='crores')

    salary_currency = models.CharField(
        max_length=10, choices=CURRENCY_CHOICES, null=True, blank=True)
    salary_per_film = models.DecimalField(
        max_digits=15, decimal_places=2, null=True, blank=True)
    salary_value_unit = models.CharField(
        max_length=8, choices=VALUE_UNIT_CHOICES, default='crores')
    salary_note = models.CharField(max_length=1255, null=True, blank=True)
    # spouse = models.OneToOneField('self', on_delete=models.SET_NULL, null=True, blank=True, related_name='married_to')
    # parents = models.ManyToManyField('self', blank=True, related_name='children', symmetrical=False)
    height = models.CharField(max_length=20, null=True, blank=True)
    weight = models.DecimalField(
        max_digits=15, decimal_places=2, null=True, blank=True, help_text="Weight in Kg")
    eye_color = models.CharField(max_length=50, null=True, blank=True)
    hair_color = models.CharField(max_length=50, null=True, blank=True)
    chest = models.CharField(max_length=50, null=True, blank=True)
    waist = models.CharField(max_length=50, null=True, blank=True)
    biceps = models.CharField(max_length=50, null=True, blank=True)
    body_figure = models.CharField(max_length=50, null=True, blank=True)
    birthplace = models.CharField(max_length=1255, null=True, blank=True)
    zodiac_sign = models.CharField(
        max_length=50, choices=ZODIAC_SIGN_CHOICES, null=True, blank=True)
    hometown = models.CharField(max_length=1255, null=True, blank=True)
    school = models.CharField(max_length=1255, null=True, blank=True)
    college = models.CharField(max_length=1255, null=True, blank=True)
    education_qualification = models.CharField(
        max_length=255, null=True, blank=True)
    ethnicity = models.CharField(max_length=100, null=True, blank=True)
    religion = models.CharField(max_length=1255, null=True, blank=True)
    caste = models.CharField(max_length=1255, null=True, blank=True)
    hobbies = models.CharField(max_length=1255, null=True, blank=True)
    vegetarian = models.BooleanField(default=False)
    favorite_food = models.CharField(max_length=1255, null=True, blank=True)
    website = models.URLField(max_length=200, null=True, blank=True)
    instagram_followers = models.DecimalField(
        max_digits=15, decimal_places=2, null=True, blank=True, help_text="Followers in Million")
    followers_unit = models.CharField(
        max_length=8, choices=FOLLOWERS_UNIT_CHOICES, default='million')
    instagram = models.URLField(max_length=200, null=True, blank=True)
    twitter = models.URLField(max_length=200, null=True, blank=True)
    facebook = models.URLField(max_length=200, null=True, blank=True)
    youtube = models.URLField(max_length=200, null=True, blank=True)

    favorite_hollywood_actor = models.CharField(
        max_length=1000, null=True, blank=True)
    favorite_bollywood_actor = models.CharField(
        max_length=1000, null=True, blank=True)
    favorite_actress = models.CharField(max_length=1000, null=True, blank=True)
    favorite_film = models.CharField(max_length=1000, null=True, blank=True)
    favorite_singer = models.CharField(max_length=1000, null=True, blank=True)
    favorite_restaurant = models.CharField(
        max_length=1000, null=True, blank=True)
    favorite_color = models.CharField(max_length=1000, null=True, blank=True)
    favorite_beverage = models.CharField(
        max_length=1000, null=True, blank=True)
    favorite_dessert = models.CharField(max_length=1000, null=True, blank=True)
    favorite_perfume = models.CharField(max_length=1000, null=True, blank=True)
    favorite_sport = models.CharField(max_length=1000, null=True, blank=True)
    favorite_cricketers = models.CharField(
        max_length=1000, null=True, blank=True)
    favorite_song = models.CharField(max_length=1000, null=True, blank=True)
    favorite_cars = models.CharField(max_length=1000, null=True, blank=True)
    favorite_outfit = models.CharField(max_length=1000, null=True, blank=True)
    favorite_fashion_brands = models.CharField(
        max_length=1000, null=True, blank=True)
    favorite_film_director = models.CharField(
        max_length=1000, null=True, blank=True)

    def __str__(self):
        return f"Biography of {self.celebrity.first_name} {self.celebrity.last_name}"


class BiographyMedia(models.Model):
    PLATFORM_TYPE_CHOICES = [
        ('instagram', 'Instagram'),
        ('twitter', 'Twitter'),
        ('youtube', 'YouTube'),
        ('facebook', 'Facebook'),
        ('pinterest', 'Pinterest'),
    ]

    BIOGRAPHY_TYPE_CHOICES = [
        ('bio/wiki', 'Bio/Wiki'),
        ('physicalStats', 'Physical Stats'),
        ('favourites', 'Favourites'),
    ]

    biography = models.OneToOneField(
        Biography, on_delete=models.CASCADE, related_name='biography_media')
    biography_type = models.CharField(
        max_length=100, choices=BIOGRAPHY_TYPE_CHOICES, default='bio/wiki')
    platform_type = models.CharField(
        max_length=100, choices=PLATFORM_TYPE_CHOICES, default='instagram')
    image = models.FileField(
        upload_to='media/celebrities/biography/', null=True, blank=True)
    embedded_code = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"Biography Media - {self.biography.celebrity.first_name} {self.biography.celebrity.last_name} - {self.biography_type}"

    class Meta:
        verbose_name = "Biography Media"
        verbose_name_plural = "Biography Media's"


class CelebrityFacts(models.Model):
    TYPE_CHOICES = [
        ('instagram', 'Instagram'),
        ('twitter', 'Twitter'),
        ('youtube', 'YouTube'),
        ('facebook', 'Facebook'),
        ('pinterest', 'Pinterest'),
    ]

    celebrity = models.ForeignKey(
        Celebrity, on_delete=models.CASCADE, related_name='celebrity_facts')
    text = models.TextField(null=True, blank=True)
    platform_type = models.CharField(
        max_length=100, choices=TYPE_CHOICES, default='instagram')
    image = models.FileField(
        upload_to='media/celebrities/facts/', null=True, blank=True)
    embedded_code = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"Celebrity Fact - {self.celebrity.first_name} {self.celebrity.last_name} - {self.platform_type}"

    class Meta:
        verbose_name = "Celebrity Fact"
        verbose_name_plural = "Celebrity Facts"


class CelebrityFAQCategory(models.Model):
    name = models.CharField(max_length=200, unique=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Celebrity FAQ Category"
        verbose_name_plural = "Celebrity FAQ Categories"


class CelebrityFAQ(models.Model):
    celebrity = models.ForeignKey(
        Celebrity, on_delete=models.CASCADE, related_name='faqs')
    category = models.ManyToManyField(
        CelebrityFAQCategory, related_name='faqs')
    question = models.TextField()
    answer = models.TextField()
    is_active = models.BooleanField(default=True)
    date_created = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)
    priority = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.category.name if self.category else 'General'}: FAQ for {self.celebrity.first_name} {self.celebrity.last_name}"

    class Meta:
        verbose_name = "Celebrity FAQ"
        verbose_name_plural = "Celebrity FAQs"
        ordering = ['priority', 'date_created']


class CelebrityRelationship(models.Model):
    RELATIONSHIP_CHOICES = [
    ('father', 'Father'),
    ('mother', 'Mother'),
    ('step_father', 'Step Father'),
    ('step_mother', 'Step Mother'),
    ('girlfriend', 'Girlfriend'),
    ('boyfriend', 'Boyfriend'),
    ('sister', 'Sister'),
    ('brother', 'Brother'),
    ('affair', 'Affair'),
    ('ex_girlfriend', 'Ex-Girlfriend'),
    ('ex_boyfriend', 'Ex-Boyfriend'),
    ('ex_spouse', 'Ex-Spouse'),
    ('husband', 'Husband'),
    ('wife', 'Wife'),
    ('son', 'Son'),
    ('daughter', 'Daughter'),
    ('step_son', 'Step Son'),
    ('step_daughter', 'Step Daughter'),
    ('grandfather', 'Grandfather'),
    ('grandmother', 'Grandmother'),
    ('grandson', 'Grandson'),
    ('granddaughter', 'Granddaughter'),
    ('uncle', 'Uncle'),
    ('aunt', 'Aunt'),
    ('nephew', 'Nephew'),
    ('niece', 'Niece'),
    ('cousin', 'Cousin'),
    ('father_in_law', 'Father-in-law'),
    ('mother_in_law', 'Mother-in-law'),
    ('brother_in_law', 'Brother-in-law'),
    ('sister_in_law', 'Sister-in-law'),
    ('son_in_law', 'Son-in-law'),
    ('daughter_in_law', 'Daughter-in-law'),
    ('step_father_in_law', 'Step Father-in-law'),
    ('step_mother_in_law', 'Step Mother-in-law'),
    ('friend', 'Friend'),
    ('mentor', 'Mentor'),
    ('protégé', 'Protégé'),
    ('business_partner', 'Business Partner'),
    ('roommate', 'Roommate'),
    ('fiance', 'Fiancé'),
    ('fiancee', 'Fiancée'),
    ('godfather', 'Godfather'),
    ('godmother', 'Godmother'),
    ('legal_guardian', 'Legal Guardian'),
    ('ward', 'Ward'),
    ('other', 'Other')
]

    celebrity = models.ForeignKey(
        Celebrity, on_delete=models.CASCADE, related_name='relationships')
    relationship_type = models.CharField(
        max_length=50, choices=RELATIONSHIP_CHOICES)

    related_celebrity = models.ForeignKey(
        Celebrity, on_delete=models.SET_NULL, null=True, blank=True, related_name='relationships_to')
    relates_relationship_type = models.CharField(
        max_length=50, choices=RELATIONSHIP_CHOICES)

    # Details for non-celebrities
    name = models.CharField(max_length=255, blank=True, null=True)
    image = models.FileField(
        upload_to='media/celebrities/celebrity_relations/', blank=True, null=True)
    embedded_code = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.celebrity.first_name} {self.celebrity.last_name} - {self.relationship_type}"

    class Meta:
        verbose_name = "Celebrity Relationship"
        verbose_name_plural = "Celebrity Relationships"


class CelebrityControversies(models.Model):
    TYPE_CHOICES = [
        ('instagram', 'Instagram'),
        ('twitter', 'Twitter'),
        ('youtube', 'YouTube'),
        ('facebook', 'Facebook'),
        ('pinterest', 'Pinterest'),
    ]

    celebrity = models.ForeignKey(
        Celebrity, on_delete=models.CASCADE, related_name='celebrity_controversies')
    heading = models.TextField(null=True, blank=True)
    text = models.TextField(null=True, blank=True)
    platform_type = models.CharField(
        max_length=100, choices=TYPE_CHOICES, default='instagram')
    image = models.FileField(
        upload_to='media/celebrities/controversies/', null=True, blank=True)
    embedded_code = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"Celebrity controversies - {self.celebrity.first_name} {self.celebrity.last_name} - {self.heading}"

    class Meta:
        verbose_name = "Celebrity Controversies"
        verbose_name_plural = "Celebrity Controversies"
