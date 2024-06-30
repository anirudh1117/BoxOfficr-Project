from django.db import models
from django.contrib.auth.models import User
from django_ckeditor_5.fields import CKEditor5Field
from utils.commonFunction import slugify


class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    name_slug = models.SlugField(blank=True, null=True, editable=False)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if self.name:
            self.name_slug = slugify(self.name.upper())
        super().save(*args, **kwargs)


class Tag(models.Model):
    name = models.CharField(max_length=100)
    name_slug = models.SlugField(blank=True, null=True, editable=False)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if self.name:
            self.name_slug = slugify(self.name.upper())
        super().save(*args, **kwargs)


class Section(models.Model):
    SECTION_TYPES = [
        ('heading', 'Heading'),
        ('subheading', 'Subheading'),
        ('paragraph', 'Paragraph'),
        ('image', 'Image'),
        ('content', 'Content'),
        ('custom', 'Custom'),
    ]

    post = models.ForeignKey(
        'Post', related_name='sections', on_delete=models.CASCADE)
    section_type = models.CharField(max_length=20, choices=SECTION_TYPES)
    content = models.TextField(blank=True)
    custom_content = CKEditor5Field(
        blank=True, null=True, config_name='extends')
    previous_section = models.OneToOneField(
        'self', related_name='next_section', on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"{self.section_type} - {self.post.title} - {self.id}"


class Image(models.Model):
    section = models.ForeignKey(
        Section, related_name='images', on_delete=models.CASCADE)
    image = models.FileField(upload_to='media/blogs/images/')
    caption = models.TextField(blank=True)

    def __str__(self):
        return f"Image for {self.section.post.title} - {self.caption}"


class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, max_length=255, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    category = models.ManyToManyField('Category')
    tags = models.ManyToManyField('Tag')
    is_published = models.BooleanField(default=False)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if self.title:
            self.slug = slugify(self.title.upper())
        super().save(*args, **kwargs)
