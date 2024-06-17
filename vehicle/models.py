from django.db import models

from celebrity.models import Celebrity
from utils.commonFunction import calculate_next_year


class VehicleMaker(models.Model):
    name = models.CharField(max_length=500)

    def __str__(self):
        return f"{self.name}"

class Vehicle(models.Model):
    VEHICLE_TYPE_CHOICES = [
        ('Car', 'Car'),
        ('Bike', 'Bike')
    ]

    YEAR_CHOICES = [(year, year)
                    for year in range(1950, calculate_next_year())]

    type = models.CharField(max_length=10, choices=VEHICLE_TYPE_CHOICES)
    make = models.ForeignKey(VehicleMaker, on_delete=models.DO_NOTHING)
    model = models.CharField(max_length=100)
    year = models.IntegerField(choices=YEAR_CHOICES)
    color = models.CharField(max_length=50, null=True, blank=True)
    engine_capacity = models.CharField(max_length=50, null=True, blank=True)
    top_speed = models.CharField(max_length=50, null=True, blank=True)
    image = models.FileField(upload_to='media/vehicles/', null=True, blank=True)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"{self.make} {self.model} ({self.year})"

class VehicleOwnership(models.Model):
    person = models.ForeignKey(Celebrity, on_delete=models.CASCADE, related_name='vehicle_ownerships')
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE, related_name='vehicle_ownerships')
    image = models.FileField(upload_to='media/vehicles/', null=True, blank=True)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.person.first_name} {self.person.last_name} owns {self.quantity} {self.vehicle.make} {self.vehicle.model}"
