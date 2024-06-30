from rest_framework import serializers
from django.utils import timezone

from movie.models import Movie

from .models import ProductRecommendation, AffiliateLink
from celebrity.models import Celebrity
from celebrity.serializer import CelebrityTagsSerializer, FilmIndustrySerializer, RoleSerializer


class AffilateLinkSerializer(serializers.ModelSerializer):

    class Meta:
        model = AffiliateLink
        fields = '__all__'

class ProductRecommendSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()
    description = serializers.SerializerMethodField()
    price = serializers.SerializerMethodField()
    price_currency = serializers.SerializerMethodField()
    product_image = serializers.SerializerMethodField()
    category = serializers.SerializerMethodField()
    brand = serializers.SerializerMethodField()
    sku = serializers.SerializerMethodField()
    likes = serializers.SerializerMethodField()
    links = serializers.SerializerMethodField()

    def get_name(self,obj):
        if obj.product and obj.product.name:
            return obj.product.name
        
        return ""
    
    def get_description(self,obj):
        if obj.product and obj.product.description:
            return obj.product.description
        
        return ""
    
    def get_price(self,obj):
        if obj.product and obj.product.price:
            return obj.product.price
        
        return ""
    
    def get_price_currency(self,obj):
        if obj.product and obj.product.price_currency:
            return obj.product.price_currency
        
        return ""
    
    def get_category(self,obj):
        if obj.product and obj.product.category:
            categories = obj.product.category.all()
            return ", ".join([category.name for category in categories])
        
        return ""
    
    def get_brand(self,obj):
        if obj.product and obj.product.brand:
            return obj.product.brand
        
        return ""
    
    def get_sku(self,obj):
        if obj.product and obj.product.sku:
            return obj.product.sku
        
        return ""
    
    def get_likes(self,obj):
        if obj.product and obj.product.likes:
            return obj.product.likes
        
        return ""
    
    def get_links(self,obj):
        if obj.product:
            linksObj = obj.product.affiliate_links.all()
            serializer = AffilateLinkSerializer(linksObj, many=True)
            return serializer.data
        
        return []
    
    def get_product_image(self, obj):
        request = self.context.get("request")
        image_url = ''
        if obj.product and obj.product.image:
            image_url = obj.product.image.url
        else:
            pass
        path = request.build_absolute_uri()
        path = path.replace('//', '/')
        path = path.split('/')
        url = path[0] + "//" + path[1] + image_url
        return url

    class Meta:
        model = ProductRecommendation
        fields = ('recommendation_reason','name','description','price','price_currency','product_image','category','brand','sku','likes','links')

class CelebrityProductRecommendSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()
    industry = FilmIndustrySerializer(many=True)
    roles = RoleSerializer(many=True)
    tags = CelebrityTagsSerializer(many=True)
    products_recommended = serializers.SerializerMethodField()
    author = serializers.SerializerMethodField()
    upcoming_movies_count = serializers.SerializerMethodField()
    recommended_products_count = serializers.SerializerMethodField()
    awards_count = serializers.SerializerMethodField()
    vehicle_collection_count = serializers.SerializerMethodField()

    def get_upcoming_movies_count(self, celebrity):
        current_date = timezone.now().date()
        return Movie.objects.filter(movie_worked__person=celebrity, release_date__gte=current_date).count()

    def get_recommended_products_count(self, celebrity):
        return celebrity.product_recommendations.count()

    def get_awards_count(self, celebrity):
        return celebrity.nominations.filter(winner=True).count()

    def get_vehicle_collection_count(self, celebrity):
        return celebrity.vehicle_ownerships.count()

    def get_author(self, celebrity):
        if celebrity.author:
            full_name = (celebrity.author.first_name if celebrity.author.first_name else '') + ' ' + (celebrity.author.last_name if celebrity.author.last_name else '')
            return full_name
        return "Admin"

    def get_image(self, celebrity):
        request = self.context.get("request")
        image_url = ''
        if celebrity.image:
            image_url = celebrity.image.url
        else:
            pass
        path = request.build_absolute_uri()
        path = path.replace('//', '/')
        path = path.split('/')
        url = path[0] + "//" + path[1] + image_url
        return url

    def get_products_recommended(self, celebrity):
        recommendedObj = celebrity.product_recommendations.all()
        if recommendedObj.first():
            serializer = ProductRecommendSerializer(
                recommendedObj, many=True,  context=self.context)
            return serializer.data

        return []

    class Meta:
        model = Celebrity
        fields = '__all__'
