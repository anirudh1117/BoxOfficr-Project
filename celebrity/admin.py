from django.contrib import admin
from .models import Celebrity, Biography, FilmIndustry, Role, CelebrityTags, CelebrityFacts, BiographyMedia, CelebrityFAQ, CelebrityFAQCategory, CelebrityRelationship, CelebrityControversies


@admin.register(Celebrity)
class CelebrityAdmin(admin.ModelAdmin):
    search_fields = ['first_name', 'last_name']


admin.site.register(Biography)
admin.site.register(FilmIndustry)
admin.site.register(Role)
admin.site.register(CelebrityTags)
admin.site.register(CelebrityFacts)
admin.site.register(BiographyMedia)


@admin.register(CelebrityFAQCategory)
class CelebrityFAQCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'description']
    search_fields = ['name', 'description']


@admin.register(CelebrityFAQ)
class CelebrityFAQAdmin(admin.ModelAdmin):
    list_display = ('celebrity', 'question',
                    'is_active', 'priority')
    list_filter = ('is_active', 'category', 'date_created')
    search_fields = ('question', 'answer', 'celebrity__first_name',
                     'celebrity__last_name', 'category__name')
    list_editable = ('is_active', 'priority')
    # raw_id_fields = ('celebrity', 'category')
    date_hierarchy = 'date_created'


@admin.register(CelebrityRelationship)
class CelebrityRelationshipAdmin(admin.ModelAdmin):
    list_display = ('celebrity', 'relationship_type',
                    'related_celebrity', 'name')
    list_filter = ('relationship_type',)
    search_fields = ('celebrity__first_name', 'celebrity__last_name',
                     'related_celebrity__first_name', 'related_celebrity__last_name', 'name')
    autocomplete_fields = ('celebrity', 'related_celebrity')


@admin.register(CelebrityControversies)
class CelebrityContoversiesAdmin(admin.ModelAdmin):
    list_display = ('celebrity',)
    search_fields = ('celebrity__first_name', 'celebrity__last_name',)
    autocomplete_fields = ('celebrity', )
