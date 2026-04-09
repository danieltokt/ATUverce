from django.db import models
from apps.users.models import User

class ChatSession(models.Model):
    """Сессия чата студента с ИИ"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='chat_sessions')
    title = models.CharField(max_length=200, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-updated_at']


class ChatMessage(models.Model):
    ROLES = [('user', 'Студент'), ('assistant', 'ИИ')]
    session = models.ForeignKey(ChatSession, on_delete=models.CASCADE, related_name='messages')
    role = models.CharField(max_length=10, choices=ROLES)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_at']