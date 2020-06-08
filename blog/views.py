from django.shortcuts import render
from .models import Post

def blogHome(request):
    context = { 'posts': Post.objects.all() , 'title': 'Blog'}

    return render(request, 'blog/blog.html', context)
