from rest_framework import serializers
from django.utils import timezone

from utils.commonFunction import calculate_age, calculate_age_difference, crore_to_million
from .models import Celebrity, Biography, Role, FilmIndustry, CelebrityTags, BiographyMedia, CelebrityFacts, CelebrityFAQ, CelebrityRelationship, CelebrityControversies
from movie.models import Movie


class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = '__all__'


class FilmIndustrySerializer(serializers.ModelSerializer):
    class Meta:
        model = FilmIndustry
        fields = '__all__'


class CelebrityTagsSerializer(serializers.ModelSerializer):

    class Meta:
        model = CelebrityTags
        fields = '__all__'


class CelebrityNameAndSlugSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()
    image = serializers.SerializerMethodField()
    roles = serializers.SerializerMethodField()

    def get_roles(self, obj):
        return ", ".join([role.name for role in obj.roles.all()])

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

    def get_name(self, obj):
        if obj:
            fullName = (obj.first_name if obj.first_name else '') + \
                ' ' + (obj.last_name if obj.last_name else '')
            return fullName

        return ""

    class Meta:
        model = Celebrity
        fields = ('name', 'celebrity_slug', 'image', 'roles')


class CelebrityDirectRelationshipSerializer(serializers.ModelSerializer):
    related_celebrity = CelebrityNameAndSlugSerializer()
    image = serializers.SerializerMethodField()

    def get_image(self, relationship):
        request = self.context.get("request")
        image_url = ''
        if relationship.image:
            image_url = relationship.image.url
        else:
            pass
        path = request.build_absolute_uri()
        path = path.replace('//', '/')
        path = path.split('/')
        url = path[0] + "//" + path[1] + image_url
        return url

    class Meta:
        model = CelebrityRelationship
        fields = ('celebrity', 'relationship_type',
                  'related_celebrity', 'name', 'image', 'embedded_code',)


class CelebrityDirectRelationshipSerializer(serializers.ModelSerializer):
    related_celebrity = CelebrityNameAndSlugSerializer()
    image = serializers.SerializerMethodField()

    def get_image(self, relationship):
        request = self.context.get("request")
        image_url = ''
        if relationship.image:
            image_url = relationship.image.url
        else:
            pass
        path = request.build_absolute_uri()
        path = path.replace('//', '/')
        path = path.split('/')
        url = path[0] + "//" + path[1] + image_url
        return url

    class Meta:
        model = CelebrityRelationship
        fields = ('celebrity', 'relationship_type',
                  'related_celebrity', 'name', 'image', 'embedded_code',)


class CelebrityInDirectRelationshipSerializer(serializers.ModelSerializer):
    related_celebrity = serializers.SerializerMethodField()
    image = serializers.SerializerMethodField()
    relationship_type = serializers.SerializerMethodField()

    def get_image(self, relationship):
        request = self.context.get("request")
        image_url = ''
        if relationship.image:
            image_url = relationship.image.url
        else:
            pass
        path = request.build_absolute_uri()
        path = path.replace('//', '/')
        path = path.split('/')
        url = path[0] + "//" + path[1] + image_url
        return url

    def get_related_celebrity(self, relationship):
        if relationship.celebrity:
            serializers = CelebrityNameAndSlugSerializer(
                relationship.celebrity)
            return serializers.data

        return {}

    def get_relationship_type(self, relationship):
        if relationship.relates_relationship_type:
            return relationship.relates_relationship_type

        return "NA"

    class Meta:
        model = CelebrityRelationship
        fields = ('celebrity', 'relationship_type',
                  'related_celebrity', 'name', 'image', 'embedded_code',)


class CelebrityControversiesSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()

    def get_image(self, facts):
        request = self.context.get("request")
        image_url = ''
        if facts.image:
            image_url = facts.image.url
        else:
            pass
        path = request.build_absolute_uri()
        path = path.replace('//', '/')
        path = path.split('/')
        url = path[0] + "//" + path[1] + image_url
        return url

    class Meta:
        model = CelebrityControversies
        fields = '__all__'


class CelebrityFactsSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()

    def get_image(self, facts):
        request = self.context.get("request")
        image_url = ''
        if facts.image:
            image_url = facts.image.url
        else:
            pass
        path = request.build_absolute_uri()
        path = path.replace('//', '/')
        path = path.split('/')
        url = path[0] + "//" + path[1] + image_url
        return url

    class Meta:
        model = CelebrityFacts
        fields = '__all__'


class CelebrityFactsSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()

    def get_image(self, facts):
        request = self.context.get("request")
        image_url = ''
        if facts.image:
            image_url = facts.image.url
        else:
            pass
        path = request.build_absolute_uri()
        path = path.replace('//', '/')
        path = path.split('/')
        url = path[0] + "//" + path[1] + image_url
        return url

    class Meta:
        model = CelebrityFacts
        fields = '__all__'


class CelebrityFAQSerializer(serializers.ModelSerializer):
    category = serializers.SerializerMethodField()

    def get_category(self, faq):
        return ", ".join([category.name for category in faq.category.all()])

    class Meta:
        model = CelebrityFAQ
        fields = '__all__'


class BiographyMediaSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()

    def get_image(self, biographymedia):
        request = self.context.get("request")
        image_url = ''
        if biographymedia.image:
            image_url = biographymedia.image.url
        else:
            pass
        path = request.build_absolute_uri()
        path = path.replace('//', '/')
        path = path.split('/')
        url = path[0] + "//" + path[1] + image_url
        return url

    class Meta:
        model = BiographyMedia
        fields = '__all__'


class CelebritySerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()
    industry = FilmIndustrySerializer(many=True)
    roles = RoleSerializer(many=True)
    tags = CelebrityTagsSerializer(many=True)
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

    class Meta:
        model = Celebrity
        fields = '__all__'


class BiographySerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()
    age = serializers.SerializerMethodField()
    weight = serializers.SerializerMethodField()
    net_worth_in_crores = serializers.SerializerMethodField()
    net_worth_in_millions = serializers.SerializerMethodField()
    instagram_followers = serializers.SerializerMethodField()
    salary_per_film_in_crores = serializers.SerializerMethodField()
    salary_per_film_in_millions = serializers.SerializerMethodField()
    biography_media = serializers.SerializerMethodField()
    celebrity_relationship = serializers.SerializerMethodField()
    celebrity_controversies = serializers.SerializerMethodField()

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

    def get_age(self, biography):
        age = ''
        if biography.date_of_death:
            age = calculate_age_difference(
                biography.date_of_birth, biography.date_of_death)
        else:
            age = calculate_age(biography.date_of_birth)

        return str(age) + ' years'

    def get_instagram_followers(self, biography):
        if biography.instagram_followers:
            return f"{biography.instagram_followers:.2f} Million"

        return "NA"

    def get_weight(self, biography):

        if biography.weight:
            return str(biography.weight) + " kg"

        return "NA"

    def get_net_worth_in_crores(self, biography):
        if biography.net_worth:
            return f"{biography.net_worth:.2f} Crores"
        return "NA"

    def get_net_worth_in_millions(self, biography):
        if biography.net_worth:
            return f"{crore_to_million(biography.net_worth):.2f} Million"
        return "NA"

    def get_salary_per_film_in_crores(self, biography):
        if biography.salary_per_film:
            return f"{biography.salary_per_film:.2f} Crores"
        return "NA"

    def get_salary_per_film_in_millions(self, biography):
        if biography.salary_per_film:
            return f"{crore_to_million(biography.salary_per_film):.2f} Million"
        return "NA"

    def get_biography_media(self, biography):
        biographyMediaArray = BiographyMedia.objects.filter(
            biography=biography)

        if biographyMediaArray.first():
            serializers = BiographyMediaSerializer(
                biographyMediaArray, many=True, context=self.context)
            return serializers.data

        return []

    def get_celebrity_relationship(self, biography):
        direct_relationship = biography.celebrity.relationships.all()
        indirect_relationship = biography.celebrity.relationships_to.all()

        if direct_relationship.first():
            serializers = CelebrityDirectRelationshipSerializer(
                direct_relationship, many=True, context=self.context)
            return serializers.data
        elif indirect_relationship.first():
            serializers = CelebrityInDirectRelationshipSerializer(
                indirect_relationship, many=True, context=self.context)
            return serializers.data

        return []

    def get_celebrity_controversies(self, biography):
        controversies = biography.celebrity.celebrity_controversies.all()

        if controversies.first():
            serializers = CelebrityControversiesSerializer(
                controversies, many=True, context=self.context)
            return serializers.data

        return []

    class Meta:
        model = Biography
        exclude = ('celebrity', 'net_worth',
                   'worth_value_unit', 'followers_unit', 'salary_value_unit', 'salary_per_film')


class CelebrityBiographySerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()
    industry = FilmIndustrySerializer(many=True)
    roles = RoleSerializer(many=True)
    tags = CelebrityTagsSerializer(many=True)
    biography = serializers.SerializerMethodField()
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
            full_name = (celebrity.author.first_name if celebrity.author.first_name else '') + \
                ' ' + (celebrity.author.last_name if celebrity.author.last_name else '')
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

    def get_biography(self, celebrity):
        biography = Biography.objects.filter(celebrity=celebrity)
        if biography.first():
            serializer = BiographySerializer(
                biography[0], context=self.context)
            return serializer.data

        return {}

    class Meta:
        model = Celebrity
        fields = '__all__'


class CelebrityFactsAndFQ(serializers.ModelSerializer):
    celebrity_facts = serializers.SerializerMethodField()
    celebrity_FQ = serializers.SerializerMethodField()

    def get_celebrity_facts(self, celebrity):
        celebrity_facts = celebrity.celebrity_facts.all()
        if celebrity_facts.first():
            serializers = CelebrityFactsSerializer(
                celebrity_facts, many=True, context=self.context)

            return serializers.data
        return []

    def get_celebrity_FQ(self, celebrity):
        celebrity_FQ = celebrity.faqs.order_by('-priority').all()
        if celebrity_FQ.first():
            serializers = CelebrityFAQSerializer(
                celebrity_FQ, many=True, context=self.context)

            return serializers.data
        return []

    class Meta:
        model = Celebrity
        fields = ('celebrity_facts', 'celebrity_FQ')
