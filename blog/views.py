from django.shortcuts import render, get_object_or_404
from .models import Post, Section

def preview_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    sections = Section.objects.filter(post=post).order_by('id')  # Ensure sections are in order
    return render(request, 'blog/preview_post.html', {'post': post, 'sections': sections})
