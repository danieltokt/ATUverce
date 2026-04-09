from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from django.utils import timezone
from .models import Story
from .serializers import StorySerializer
from apps.coins.utils import award_coins

class StoryListView(generics.ListCreateAPIView):
    serializer_class = StorySerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Story.objects.filter(expires_at__gt=timezone.now()).select_related('author')

    def perform_create(self, serializer):
        story = serializer.save(author=self.request.user)
        award_coins(self.request.user, 'story_posted', f'Выложил сторис #{story.id}')