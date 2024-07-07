from django.contrib import admin
from .models import Celebrity, Biography, FilmIndustry, Role, CelebrityTags, CelebrityFacts, BiographyMedia, CelebrityFAQ, CelebrityFAQCategory, CelebrityRelationship, CelebrityControversies


@admin.register(Celebrity)
class CelebrityAdmin(admin.ModelAdmin):
    search_fields = ['first_name', 'last_name']
    list_display = ('first_name', 'last_name', 'is_published', 'created_at')
    list_filter = ('is_published', 'created_at', 'industry', 'roles', 'tags')
    filter_horizontal = ('industry', 'roles', 'tags')


@admin.register(FilmIndustry)
class FilmIndustryAdmin(admin.ModelAdmin):
    list_display = ('name', 'name_slug')
    search_fields = ('name',)


@admin.register(CelebrityTags)
class CelebrityTagsAdmin(admin.ModelAdmin):
    list_display = ('name', 'name_slug')
    search_fields = ('name',)


@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    list_display = ('name', 'name_slug')
    search_fields = ('name',)


@admin.register(Biography)
class BiographyAdmin(admin.ModelAdmin):
    list_display = ('celebrity', 'date_of_birth', 'nationality', 'gender')
    search_fields = ('celebrity__first_name',
                     'celebrity__last_name', 'nationality')
    list_filter = ('gender', 'marital_status', 'nationality',
                   'celebrity', 'celebrity__roles', 'celebrity__industry', 'celebrity__tags')


@admin.register(BiographyMedia)
class BiographyMediaAdmin(admin.ModelAdmin):
    list_display = ('biography', 'biography_type', 'platform_type')
    search_fields = ('biography__celebrity__first_name',
                     'biography__celebrity__last_name')
    list_filter = ('biography_type', 'platform_type', 'biography')
    fieldsets = (
        ("general", {"fields": ("biography", "biography_type",)}),
        ("image", {"fields": ("image","alt_text",)}),
        ("embedded code", {"fields": ("platform_type","embedded_code",)}),
    )


@admin.register(CelebrityFacts)
class CelebrityFactsAdmin(admin.ModelAdmin):
    list_display = ('celebrity', 'platform_type', 'text')
    search_fields = ('celebrity__first_name', 'celebrity__last_name')
    list_filter = ('platform_type', 'celebrity',)
    fieldsets = (
        ("general", {"fields": ("celebrity", "text",)}),
        ("image", {"fields": ("image","alt_text",)}),
        ("embedded code", {"fields": ("platform_type","embedded_code",)}),
    )


@admin.register(CelebrityFAQCategory)
class CelebrityFAQCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'description']
    search_fields = ['name', 'description']


@admin.register(CelebrityFAQ)
class CelebrityFAQAdmin(admin.ModelAdmin):
    list_display = ('celebrity', 'question',
                    'is_active', 'priority')
    list_filter = ('is_active', 'category', 'date_created', 'celebrity')
    search_fields = ('question', 'answer', 'celebrity', 'category')
    list_editable = ('is_active', 'priority')
    # raw_id_fields = ('celebrity', 'category')
    date_hierarchy = 'date_created'


@admin.register(CelebrityRelationship)
class CelebrityRelationshipAdmin(admin.ModelAdmin):
    list_display = ('celebrity', 'relationship_type',
                    'related_celebrity', 'name')
    list_filter = ('relationship_type', 'celebrity',)
    search_fields = ('celebrity__first_name', 'celebrity__last_name',
                     'related_celebrity__first_name', 'related_celebrity__last_name', 'name')
    autocomplete_fields = ('celebrity', 'related_celebrity')
    fieldsets = (
        ("general", {"fields": ("celebrity", "relationship_type","related_celebrity","relates_relationship_type","name",)}),
        ("image", {"fields": ("image","alt_text",)}),
        ("embedded code", {"fields": ("embedded_code",)}),
    )


@admin.register(CelebrityControversies)
class CelebrityContoversiesAdmin(admin.ModelAdmin):
    list_display = ('celebrity', 'heading', 'platform_type')
    search_fields = ('celebrity__first_name',
                     'celebrity__last_name', 'heading')
    list_filter = ('platform_type', 'celebrity',)
    fieldsets = (
        ("general", {"fields": ("celebrity","heading", "text",)}),
        ("image", {"fields": ("image","alt_text",)}),
        ("embedded code", {"fields": ("platform_type","embedded_code",)}),
    )
