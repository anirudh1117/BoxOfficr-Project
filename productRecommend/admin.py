from django.contrib import admin
from .models import AffiliateLink, ProductRecommendation,Product,Category


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'brand')
    search_fields = ('name', 'description', 'category', 'brand')
    list_filter = ('price', 'category', 'brand')

@admin.register(ProductRecommendation)
class ProductRecommendationAdmin(admin.ModelAdmin):
    list_display = ('person', 'product', 'recommendation_reason')
    search_fields = ('person__first_name', 'person__last_name', 'product__name')
    list_filter = ('person', 'product')

@admin.register(AffiliateLink)
class AffiliateLinkAdmin(admin.ModelAdmin):
    list_display = ('product', 'platform', 'link')
    search_fields = ('product__name', 'platform')
    list_filter = ('platform',)

admin.site.register(Category)