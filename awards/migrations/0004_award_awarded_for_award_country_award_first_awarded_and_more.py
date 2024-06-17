# Generated by Django 5.0.6 on 2024-06-15 10:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('awards', '0003_award_name_slug_awardcategory_name_slug_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='award',
            name='awarded_for',
            field=models.CharField(blank=True, max_length=500),
        ),
        migrations.AddField(
            model_name='award',
            name='country',
            field=models.CharField(choices=[('India', 'India'), ('USA', 'USA'), ('UK', 'UK'), ('China', 'China'), ('Worldwide', 'Worldwide')], default='India', max_length=20),
        ),
        migrations.AddField(
            model_name='award',
            name='first_awarded',
            field=models.CharField(blank=True, max_length=500),
        ),
        migrations.AddField(
            model_name='award',
            name='last_awarded',
            field=models.CharField(blank=True, max_length=500),
        ),
        migrations.AddField(
            model_name='award',
            name='presented_by',
            field=models.CharField(blank=True, max_length=500),
        ),
        migrations.AddField(
            model_name='award',
            name='website',
            field=models.URLField(blank=True, null=True),
        ),
    ]
