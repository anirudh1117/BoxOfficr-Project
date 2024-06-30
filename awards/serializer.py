from rest_framework import serializers
from django.utils import timezone

from movie.models import Movie

from .models import Nomination, Award, AwardCategory, AwardEvent
from celebrity.models import Celebrity
from celebrity.serializer import CelebrityTagsSerializer, FilmIndustrySerializer, RoleSerializer, CelebritySerializer
from movie.serializer import MovieShortSerilaizer


class NominationSerializer(serializers.ModelSerializer):
    category = serializers.SerializerMethodField()
    year = serializers.SerializerMethodField()
    movie = serializers.SerializerMethodField()
    award_name = serializers.SerializerMethodField()
    award_title = serializers.SerializerMethodField()

    def get_award_name(self, nominationObj):
        awardObj = nominationObj.category
        if awardObj:
            awardObj = awardObj.award
            if awardObj:
                return awardObj.name

        return ""

    def get_award_title(self, nominationObj):
        awardEventObj = nominationObj.event
        if awardEventObj and awardEventObj.title:
            return awardEventObj.title

        return ""

    def get_category(self, nominationObj):
        awardCategoryObj = nominationObj.category
        if awardCategoryObj and awardCategoryObj.name:
            return awardCategoryObj.name
        return ""

    def get_year(self, nominationObj):
        awardEventObj = nominationObj.event
        if awardEventObj:
            return awardEventObj.year
        return ""

    def get_movie(self, nominationObj):
        movieObj = nominationObj.movie
        if movieObj:
            serializer = MovieShortSerilaizer(
                movieObj,  context=self.context)
            return serializer.data

        return {}

    class Meta:
        model = Nomination
        fields = '__all__'


class CelebrityAwardsSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()
    industry = FilmIndustrySerializer(many=True)
    roles = RoleSerializer(many=True)
    tags = CelebrityTagsSerializer(many=True)
    awards = serializers.SerializerMethodField()
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

    def get_awards(self, celebrity):
        nominationObj = celebrity.nominations.filter(winner=True)
        if nominationObj.first():
            serializer = NominationSerializer(
                nominationObj, many=True,  context=self.context)
            return serializer.data

        return []

    class Meta:
        model = Celebrity
        fields = '__all__'


class AwardListSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()

    def get_image(self, award):
        request = self.context.get("request")
        image_url = ''
        if award.image:
            image_url = award.image.url
        else:
            pass
        path = request.build_absolute_uri()
        path = path.replace('//', '/')
        path = path.split('/')
        url = path[0] + "//" + path[1] + image_url
        return url

    class Meta:
        model = Award
        fields = '__all__'


class AwardCategoySerializer(serializers.ModelSerializer):

    class Meta:
        model = AwardCategory
        fields = '__all__'


class AwardSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()
    award_events = serializers.SerializerMethodField()
    awards_categories = serializers.SerializerMethodField()

    def get_image(self, award):
        request = self.context.get("request")
        image_url = ''
        if award.image:
            image_url = award.image.url
        else:
            pass
        path = request.build_absolute_uri()
        path = path.replace('//', '/')
        path = path.split('/')
        url = path[0] + "//" + path[1] + image_url
        return url

    def get_award_events(self, award):
        awardEvents = award.events.all().order_by('-year')
        if awardEvents.first():
            serializer = AwardEventListSerializer(
                awardEvents, many=True,  context=self.context)
            return serializer.data

        return []

    def get_awards_categories(self, award):
        awardCategories = award.categories.all()
        if awardCategories.first():
            serializer = AwardCategoySerializer(
                awardCategories, many=True,  context=self.context)
            return serializer.data

        return []

    class Meta:
        model = Award
        fields = '__all__'


class AwardEventListSerializer(serializers.ModelSerializer):
    poster = serializers.SerializerMethodField()

    def get_poster(self, awardEvent):
        request = self.context.get("request")
        image_url = ''
        if awardEvent.poster:
            image_url = awardEvent.poster.url
        else:
            pass
        path = request.build_absolute_uri()
        path = path.replace('//', '/')
        path = path.split('/')
        url = path[0] + "//" + path[1] + image_url
        return url

    class Meta:
        model = AwardEvent
        fields = '__all__'


class AwardEventSerializer(serializers.ModelSerializer):
    poster = serializers.SerializerMethodField()
    nominations = serializers.SerializerMethodField()

    def get_poster(self, awardEvent):
        request = self.context.get("request")
        image_url = ''
        if awardEvent.poster:
            image_url = awardEvent.poster.url
        else:
            pass
        path = request.build_absolute_uri()
        path = path.replace('//', '/')
        path = path.split('/')
        url = path[0] + "//" + path[1] + image_url
        return url

    def get_nominations(self, awardEvent):
        nominations = awardEvent.nominations.all()
        if nominations.first():
            serializer = NominationListSerializer(
                nominations, many=True,  context=self.context)
            return serializer.data

        return []

    class Meta:
        model = AwardEvent
        fields = '__all__'


class NominationListSerializer(serializers.ModelSerializer):
    movie = serializers.SerializerMethodField()
    person = serializers.SerializerMethodField()

    def get_movie(self, nominationObj):
        movieObj = nominationObj.movie
        if movieObj:
            serializer = MovieShortSerilaizer(
                movieObj,  context=self.context)
            return serializer.data

        return {}

    def get_person(self, nominationObj):
        personObj = nominationObj.person
        if personObj:
            serializer = CelebritySerializer(
                personObj,  context=self.context)
            return serializer.data

        return {}

    class Meta:
        model = Nomination
        fields = '__all__'
