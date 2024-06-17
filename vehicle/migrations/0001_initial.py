# Generated by Django 5.0.6 on 2024-06-14 17:57

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('celebrity', '0004_delete_award_delete_movie'),
    ]

    operations = [
        migrations.CreateModel(
            name='VehicleMaker',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=500)),
            ],
        ),
        migrations.CreateModel(
            name='Vehicle',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(choices=[('Car', 'Car'), ('Bike', 'Bike')], max_length=10)),
                ('model', models.CharField(max_length=100)),
                ('year', models.IntegerField(choices=[(1950, 1950), (1951, 1951), (1952, 1952), (1953, 1953), (1954, 1954), (1955, 1955), (1956, 1956), (1957, 1957), (1958, 1958), (1959, 1959), (1960, 1960), (1961, 1961), (1962, 1962), (1963, 1963), (1964, 1964), (1965, 1965), (1966, 1966), (1967, 1967), (1968, 1968), (1969, 1969), (1970, 1970), (1971, 1971), (1972, 1972), (1973, 1973), (1974, 1974), (1975, 1975), (1976, 1976), (1977, 1977), (1978, 1978), (1979, 1979), (1980, 1980), (1981, 1981), (1982, 1982), (1983, 1983), (1984, 1984), (1985, 1985), (1986, 1986), (1987, 1987), (1988, 1988), (1989, 1989), (1990, 1990), (1991, 1991), (1992, 1992), (1993, 1993), (1994, 1994), (1995, 1995), (1996, 1996), (1997, 1997), (1998, 1998), (1999, 1999), (2000, 2000), (2001, 2001), (2002, 2002), (2003, 2003), (2004, 2004), (2005, 2005), (2006, 2006), (2007, 2007), (2008, 2008), (2009, 2009), (2010, 2010), (2011, 2011), (2012, 2012), (2013, 2013), (2014, 2014), (2015, 2015), (2016, 2016), (2017, 2017), (2018, 2018), (2019, 2019), (2020, 2020), (2021, 2021), (2022, 2022), (2023, 2023), (2024, 2024)])),
                ('color', models.CharField(blank=True, max_length=50, null=True)),
                ('engine_capacity', models.CharField(blank=True, max_length=50, null=True)),
                ('top_speed', models.CharField(blank=True, max_length=50, null=True)),
                ('image', models.FileField(blank=True, null=True, upload_to='media/vehicles/')),
                ('description', models.TextField(blank=True, null=True)),
                ('make', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='vehicle.vehiclemaker')),
            ],
        ),
        migrations.CreateModel(
            name='VehicleOwnership',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.FileField(blank=True, null=True, upload_to='media/vehicles/')),
                ('quantity', models.PositiveIntegerField(default=1)),
                ('person', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='vehicle_ownerships', to='celebrity.celebrity')),
                ('vehicle', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='vehicle_ownerships', to='vehicle.vehicle')),
            ],
        ),
    ]
