from django.urls import path
from .views import preview_post

urlpatterns = [
    path('admin/preview/<int:post_id>/', preview_post, name='preview_post')
]
