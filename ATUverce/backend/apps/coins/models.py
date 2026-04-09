from django.db import models
from apps.users.models import User

class CoinTransaction(models.Model):
    """История транзакций Ala Coins"""
    REASONS = [
        ('post_created', 'Создал пост'),
        ('helpful_answer', 'Помог другому студенту'),
        ('activity', 'Активность'),
        ('comment', 'Оставил комментарий'),
        ('story_posted', 'Выложил историю'),
        ('club_participation', 'Участие в клубе'),
        ('admin_bonus', 'Бонус от администрации'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='coin_transactions')
    amount = models.IntegerField()  # Может быть отрицательным (списание)
    reason = models.CharField(max_length=30, choices=REASONS)
    description = models.CharField(max_length=200, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def str(self):
        return f"{self.user.username}: {'+' if self.amount > 0 else ''}{self.amount} монет ({self.get_reason_display()})"