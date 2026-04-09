from django.db import models
from apps.users.models import User

class Post(models.Model):
    """Пост в ленте — текст, фото или видео"""
    POST_TYPES = [('text', 'Текст'), ('image', 'Фото'), ('video', 'Видео')]

    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    content = models.TextField(max_length=2000)
    post_type = models.CharField(max_length=10, choices=POST_TYPES, default='text')
    media = models.FileField(upload_to='posts/', blank=True, null=True)
    tags = models.JSONField(default=list, blank=True)
    
    likes_count = models.PositiveIntegerField(default=0)
    comments_count = models.PositiveIntegerField(default=0)
    views_count = models.PositiveIntegerField(default=0)
    
    is_pinned = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def str(self):
        return f"{self.author.username}: {self.content[:50]}"


class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='likes')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'post')


class Comment(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE)
    content = models.TextField(max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_at']