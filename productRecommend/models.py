from django.db import models

from celebrity.models import Celebrity
from utils.commonFunction import slugify

class Category(models.Model):
    name = models.CharField(max_length=300)
    name_slug = models.SlugField(blank=True, null=True, editable=False)

    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if self.name:
            self.name_slug = slugify(self.name.upper())
        super().save(*args, **kwargs)
    

class Product(models.Model):
    CURRENCY_CHOICES = [
        ('USD', 'USD'),
        ('INR', 'INR'),
        ('EUR', 'EUR'),
        ('GBP', 'GBP'),
        ('JPY', 'JPY'),
        ('Other', 'Other')
    ]

    name = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    price_currency = models.CharField(max_length=10, choices=CURRENCY_CHOICES, null=True, blank=True)
    image = models.FileField(upload_to='media/products/', null=True, blank=True)
    category = models.ManyToManyField(Category, null=True)
    brand = models.CharField(max_length=100, null=True, blank=True)
    sku = models.CharField(max_length=100, null=True, blank=True)
    likes = models.IntegerField(default=0)

    def __str__(self):
        return self.name

class AffiliateLink(models.Model):
    PLATFORM_CHOICES = [
        ('Amazon', 'Amazon'),
        ('eBay', 'eBay'),
        ('Walmart', 'Walmart'),
        ('Flipkart', 'Flipkart'),
        ('Other', 'Other')
    ]

    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='affiliate_links')
    platform = models.CharField(max_length=50, choices=PLATFORM_CHOICES)
    link = models.URLField(max_length=200)

    def __str__(self):
        return f"{self.product.name} - {self.platform}"

class ProductRecommendation(models.Model):
    person = models.ForeignKey(Celebrity, on_delete=models.CASCADE, related_name='product_recommendations')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='product_recommendations')
    recommendation_reason = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"{self.person.first_name} {self.person.last_name} recommends {self.product.name}"