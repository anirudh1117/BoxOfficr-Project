# Generated by Django 5.0.6 on 2024-06-30 19:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('celebrity', '0019_celebritycontroversies'),
    ]

    operations = [
        migrations.AlterField(
            model_name='celebrity',
            name='tags',
            field=models.ManyToManyField(blank=True, related_name='celebrities_tags', to='celebrity.celebritytags'),
        ),
    ]
