from django.urls import path
from . import views

urlpatterns = [
    path('', views.blogHome, name='blog-page'),
    path('<id>/', views.blogDetails, name='blog-detail-page'),
    path('author/<author_id>/', views.authorBlogs, name='author-blogs-page'),
    path('like/<id>/', views.likePost, name='post_like'),
    path('dislike/<id>/', views.dislikePost, name='post_dislike'),
    path('updatecomment/<comment_id>/', views.updateComment, name='update_comment'),
    path('deletecomment/<comment_id>', views.deleteComment, name='delete_comment')
]