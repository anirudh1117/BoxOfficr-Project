# Generated by Django 5.0.6 on 2024-06-11 19:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('celebrity', '0003_remove_celebrity_industry_alter_celebrity_roles_and_more'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Award',
        ),
        migrations.DeleteModel(
            name='Movie',
        ),
    ]
