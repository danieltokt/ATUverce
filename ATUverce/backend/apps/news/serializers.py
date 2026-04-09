from rest_framework import serializers
from .models import News
from apps.users.serializers import UserShortSerializer

class NewsSerializer(serializers.ModelSerializer):
    author = UserShortSerializer(read_only=True)

    class Meta:
        model = News
        fields = ['id', 'title', 'content', 'category', 'image', 'author',
                  'event_date', 'is_published', 'views_count', 'created_at']
        read_only_fields = ['author', 'views_count']