from django.contrib import admin
from .models import Post, PostLikes, PostDislikes, PostComment

admin.site.register(Post)
admin.site.register(PostLikes)
admin.site.register(PostDislikes)
admin.site.register(PostComment)
