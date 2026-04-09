from rest_framework import serializers
from .models import Story
from apps.users.serializers import UserShortSerializer

class StorySerializer(serializers.ModelSerializer):
    author = UserShortSerializer(read_only=True)
    is_active = serializers.ReadOnlyField()

    class Meta:
        model = Story
        fields = ['id', 'author', 'media', 'media_type', 'text_overlay',
                  'views_count', 'expires_at', 'created_at', 'is_active']
        read_only_fields = ['author', 'views_count']