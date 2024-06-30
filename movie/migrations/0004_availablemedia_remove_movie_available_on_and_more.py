# Generated by Django 5.0.6 on 2024-06-22 12:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movie', '0003_movie_available_on'),
    ]

    operations = [
        migrations.CreateModel(
            name='AvailableMedia',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True)),
                ('name_slug', models.SlugField(blank=True, editable=False, null=True)),
            ],
        ),
        migrations.RemoveField(
            model_name='movie',
            name='available_on',
        ),
        migrations.AddField(
            model_name='movie',
            name='available_on',
            field=models.ManyToManyField(null=True, related_name='movies', to='movie.availablemedia'),
        ),
    ]