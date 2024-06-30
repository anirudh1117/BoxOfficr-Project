# Generated by Django 5.0.6 on 2024-06-30 19:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movie', '0007_remove_boxoffice_collection_currency_boxoffice_day_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Language',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='MovieTags',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True)),
                ('name_slug', models.SlugField(blank=True, editable=False, null=True)),
            ],
        ),
        migrations.AddField(
            model_name='movie',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AddField(
            model_name='movie',
            name='universal_rating',
            field=models.CharField(blank=True, choices=[('G', 'General Audiences – All Ages Admitted'), ('PG', 'Parental Guidance Suggested – Some Material May Not Be Suitable for Children'), ('PG-13', 'Parents Strongly Cautioned – Some Material May Be Inappropriate for Children Under 13'), ('R', 'Restricted – Under 17 Requires Accompanying Parent or Adult Guardian'), ('NC-17', 'Adults Only – No One 17 and Under Admitted'), ('NR', 'Not Rated')], help_text='Universal content rating', max_length=5, null=True),
        ),
        migrations.AddField(
            model_name='movie',
            name='updated_at',
            field=models.DateTimeField(auto_now=True, null=True),
        ),
        migrations.RemoveField(
            model_name='movie',
            name='language',
        ),
        migrations.AddField(
            model_name='movie',
            name='tags',
            field=models.ManyToManyField(blank=True, related_name='movie_tags', to='movie.movietags'),
        ),
        migrations.AddField(
            model_name='movie',
            name='language',
            field=models.ManyToManyField(blank=True, to='movie.language'),
        ),
    ]
