# Generated by Django 5.0.6 on 2024-06-30 13:04

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('celebrity', '0015_alter_celebrityfacts_celebrity'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='SpotlightCelebrities',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('heading', models.TextField(blank=True, help_text='Optional Heading', null=True)),
                ('description', models.TextField(blank=True, help_text='Optional description or highlight text.', null=True)),
                ('active', models.BooleanField(default=True, help_text='Toggle visibility')),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
                ('author', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('celebrity', models.ManyToManyField(related_name='spotlight_celebrities', to='celebrity.celebrity')),
            ],
            options={
                'verbose_name': 'Spotlight Celebrity',
                'verbose_name_plural': 'Spotlight Celebrities',
            },
        ),
    ]
