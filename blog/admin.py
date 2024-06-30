from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html
from django_ckeditor_5.fields import CKEditor5Field
from django_ckeditor_5.widgets import CKEditor5Widget

from .models import Post, Section, Category, Tag, Image


class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'preview_button')
    list_filter = ('category', 'tags', 'author')
    ordering = ('-created_at',)
    search_fields = ('title',)
    autocomplete_fields = ['author']

    def preview_button(self, obj):
        return format_html('<a class="button" href="{}" target="_blank">Preview Post</a>',
                           reverse('preview_post', args=[obj.id]))

    preview_button.short_description = 'Preview'
    preview_button.allow_tags = True


admin.site.register(Post, PostAdmin)


class SectionAdmin(admin.ModelAdmin):
    list_display = ('post', 'section_type', 'content', 'previous_section')
    #autocomplete_fields = ['post', 'previous_section']

    formfield_overrides = {
        CKEditor5Field: {'widget': CKEditor5Widget(config_name='default')},
    }


admin.site.register(Section, SectionAdmin)


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')


admin.site.register(Category, CategoryAdmin)


class TagAdmin(admin.ModelAdmin):
    list_display = ('name',)


admin.site.register(Tag, TagAdmin)


class ImageAdmin(admin.ModelAdmin):
    list_display = ('section', 'caption', 'image')
    #autocomplete_fields = ['section']


admin.site.register(Image, ImageAdmin)
