# Generated by Django 5.0.6 on 2024-06-22 15:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movie', '0005_alter_movie_poster'),
    ]

    operations = [
        migrations.AlterField(
            model_name='movie',
            name='available_on',
            field=models.ManyToManyField(related_name='movies', to='movie.availablemedia'),
        ),
    ]
