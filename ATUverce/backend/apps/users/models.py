from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    """Пользователь ATUverce — студент колледжа Ала-Тоо"""
    ROLES = [('student', 'Студент'), ('teacher', 'Преподаватель'), ('admin', 'Администратор')]

    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    bio = models.TextField(blank=True, max_length=500)
    role = models.CharField(max_length=20, choices=ROLES, default='student')
    group = models.CharField(max_length=50, blank=True)  # Группа студента
    faculty = models.CharField(max_length=100, blank=True)
    year_of_study = models.PositiveSmallIntegerField(null=True, blank=True)
    
    # LinkedIn-стиль
    skills = models.JSONField(default=list, blank=True)  # ['Python', 'Design', ...]
    interests = models.JSONField(default=list, blank=True)
    github = models.URLField(blank=True)
    linkedin = models.URLField(blank=True)
    portfolio = models.URLField(blank=True)
    
    # Статистика
    followers_count = models.PositiveIntegerField(default=0)
    following_count = models.PositiveIntegerField(default=0)
    ala_coins = models.PositiveIntegerField(default=0)  # Монеты Ала-Тоо
    
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def str(self):
        return f"{self.get_full_name()} (@{self.username})"


class Follow(models.Model):
    follower = models.ForeignKey(User, related_name='following', on_delete=models.CASCADE)
    following = models.ForeignKey(User, related_name='followers', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('follower', 'following')