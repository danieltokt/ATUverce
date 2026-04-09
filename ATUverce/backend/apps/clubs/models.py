from django.db import models
from apps.users.models import User

class Club(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    logo = models.ImageField(upload_to='clubs/', blank=True, null=True)
    president = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='led_clubs')
    members = models.ManyToManyField(User, related_name='clubs', blank=True)
    members_count = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def str(self):
        return self.name


class ClubEvent(models.Model):
    club = models.ForeignKey(Club, on_delete=models.CASCADE, related_name='events')
    title = models.CharField(max_length=200)
    description = models.TextField()
    event_date = models.DateTimeField()
    location = models.CharField(max_length=200, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)