from rest_framework import serializers

from utils.commonFunction import calculate_age, calculate_age_difference
from .models import Celebrity, Biography, Role, FilmIndustry


class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = '__all__'


class FilmIndustrySerializer(serializers.ModelSerializer):
    class Meta:
        model = FilmIndustry
        fields = '__all__'


class CelebritySerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()
    industry = FilmIndustrySerializer(many=True)
    roles = RoleSerializer(many=True)

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
            age = calculate_age_difference(biography.date_of_birth, biography.date_of_death)
        else:
            age = calculate_age(biography.date_of_birth)
        
        return str(age) + ' years'

    class Meta:
        model = Biography
        exclude = ('celebrity',)


class CelebrityBiographySerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()
    industry = FilmIndustrySerializer(many=True)
    roles = RoleSerializer(many=True)
    biography = serializers.SerializerMethodField()

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
        print(biography)
        if biography.first():
            serializer = BiographySerializer(
                biography[0], context=self.context)
            return serializer.data

        return {}

    class Meta:
        model = Celebrity
        fields = '__all__'


class CelebrityNameAndSlugSerializer(serializers.ModelSerializer):
    name  = serializers.SerializerMethodField()

    def get_name(self, obj):
        if obj:
            fullName = (obj.first_name if obj.first_name else '') + ' ' + (obj.last_name if obj.last_name else '')
            return fullName
        
        return ""

    class Meta:
        model = Celebrity
        fields = ('name','celebrity_slug')
