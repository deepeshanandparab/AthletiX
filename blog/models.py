from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

class Post(models.Model):
    STATUS_CHOICES = (
        ('act', 'Active'),
        ('report', 'Report')
    )

    title = models.CharField(max_length=100)
    content = models.TextField()
    posted_on = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    cover_image = models.ImageField(default='no_image.jpg', upload_to='images/cover_images')
    likes = models.ManyToManyField(User, related_name='likes', blank=True)
    dislikes = models.ManyToManyField(User, related_name='dislikes', blank=True)
    comments = models.IntegerField(default=0)
    status = models.CharField(max_length=6, choices=STATUS_CHOICES, default='active')

    def __str__(self):
        return self.title


class PostComment(models.Model):
    user = models.ForeignKey(User, models.SET_NULL, blank=True, null=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.username} commented on post : "{self.post.title}"'



class PostLikes(models.Model):
    post_id = models.ForeignKey(Post, on_delete=models.CASCADE)
    user_id = models.ForeignKey(User, on_delete=models.DO_NOTHING)

    def __str__(self):
        return f'{self.user_id} liked post number : {self.post_id.id}'


class PostDislikes(models.Model):
    post_id = models.ForeignKey(Post, on_delete=models.CASCADE)
    user_id = models.ForeignKey(User, on_delete=models.DO_NOTHING)

    def __str__(self):
        return f'{self.user_id} disliked post number : {self.post_id.id}'
