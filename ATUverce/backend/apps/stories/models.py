from django.db import models
from django.utils import timezone
from datetime import timedelta
from apps.users.models import User

def story_expires():
    return timezone.now() + timedelta(hours=24)
class Story(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='stories')
    media = models.FileField(upload_to='stories/')
    media_type = models.CharField(max_length=10, choices=[('image','Фото'),('video','Видео')])
    text_overlay = models.CharField(max_length=200, blank=True)
    views_count = models.PositiveIntegerField(default=0)
    expires_at = models.DateTimeField(default=story_expires)
    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def is_active(self):
        return timezone.now() < self.expires_at

    class Meta:
        ordering = ['-created_at']
        verbose_name_plural = 'Stories'