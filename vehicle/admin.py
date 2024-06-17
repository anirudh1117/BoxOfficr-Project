from django.contrib import admin
from .models import Vehicle, VehicleOwnership,VehicleMaker


@admin.register(Vehicle)
class VehicleAdmin(admin.ModelAdmin):
    list_display = ('make', 'model', 'year', 'type')
    search_fields = ('make__name', 'model', 'year', 'type')
    list_filter = ('year', 'make__name', 'type')

@admin.register(VehicleOwnership)
class VehicleOwnershipAdmin(admin.ModelAdmin):
    list_display = ('person', 'vehicle', 'quantity')
    search_fields = ('person__first_name', 'person__last_name', 'vehicle__make', 'vehicle__model')

admin.site.register(VehicleMaker)