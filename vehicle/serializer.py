from rest_framework import serializers

from celebrity.serializer import FilmIndustrySerializer, RoleSerializer

from .models import Vehicle, VehicleMaker,VehicleOwnership
from celebrity.models import Celebrity

class VechicleSerializer(serializers.ModelSerializer):
    type = serializers.SerializerMethodField()
    make = serializers.SerializerMethodField()
    year = serializers.SerializerMethodField()
    model = serializers.SerializerMethodField()
    color = serializers.SerializerMethodField()
    engine_capacity = serializers.SerializerMethodField()
    top_speed = serializers.SerializerMethodField()
    vechicle_image = serializers.SerializerMethodField()
    description = serializers.SerializerMethodField()
    celebriy_image = serializers.SerializerMethodField()

    def get_type(self,obj):
        if obj.vehicle and obj.vehicle.type:
            return obj.vehicle.type

        return ""
    
    def get_make(self,obj):
        if obj.vehicle and obj.vehicle.make:
            if obj.vehicle.make:
                return obj.vehicle.make.name

        return ""
    
    def get_model(self,obj):
        if obj.vehicle and obj.vehicle.model:
            return obj.vehicle.model

        return ""
    
    def get_year(self,obj):
        if obj.vehicle and obj.vehicle.year:
            return obj.vehicle.year

        return ""
    
    def get_color(self,obj):
        if obj.vehicle and obj.vehicle.color:
            return obj.vehicle.color

        return ""
    
    def get_engine_capacity(self,obj):
        if obj.vehicle and obj.vehicle.engine_capacity:
            return obj.vehicle.engine_capacity

        return ""
    
    def get_top_speed(self,obj):
        if obj.vehicle and obj.vehicle.top_speed:
            return obj.vehicle.top_speed

        return ""
    
    def get_description(self,obj):
        if obj.vehicle and obj.vehicle.description:
            return obj.vehicle.description

        return ""
    
    def get_vechicle_image(self, obj):
        request = self.context.get("request")
        image_url = ''
        if obj.vehicle and obj.vehicle.image:
            image_url = obj.vehicle.image.url
        else:
            pass
        path = request.build_absolute_uri()
        path = path.replace('//', '/')
        path = path.split('/')
        url = path[0] + "//" + path[1] + image_url
        return url
    
    def get_celebriy_image(self, obj):
        request = self.context.get("request")
        image_url = ''
        if obj.image:
            image_url = obj.image.url
        else:
            pass
        path = request.build_absolute_uri()
        path = path.replace('//', '/')
        path = path.split('/')
        url = path[0] + "//" + path[1] + image_url
        return url


    class Meta:
        model = VehicleOwnership
        fields = ('type','make','year','model','color','engine_capacity','top_speed','vechicle_image','description','celebriy_image','quantity')


class CelebrityVechicleSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()
    industry = FilmIndustrySerializer(many=True)
    roles = RoleSerializer(many=True)
    vechicle_Collection = serializers.SerializerMethodField()

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

    def get_vechicle_Collection(self, celebrity):
        vechicleObj = celebrity.vehicle_ownerships.all()
        if vechicleObj.first():
            serializer = VechicleSerializer(
                vechicleObj, many=True,  context=self.context)
            return serializer.data

        return []


    class Meta:
        model = Celebrity
        fields = '__all__'