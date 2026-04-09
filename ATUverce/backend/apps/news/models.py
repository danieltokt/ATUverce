from django.db import models
from apps.users.models import User

class News(models.Model):
    CATEGORIES = [
        ('announcement', 'Объявление'),
        ('event', 'Событие'),
        ('achievement', 'Достижение'),
        ('scholarship', 'Стипендия'),
        ('general', 'Общее'),
    ]
    title = models.CharField(max_length=200)
    content = models.TextField()
    category = models.CharField(max_length=20, choices=CATEGORIES, default='general')
    image = models.ImageField(upload_to='news/', blank=True, null=True)
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    event_date = models.DateTimeField(null=True, blank=True)
    is_published = models.BooleanField(default=True)
    views_count = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def str(self):
        return self.title