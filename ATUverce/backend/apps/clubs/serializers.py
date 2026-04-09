from rest_framework import serializers
from .models import Club, ClubEvent
from apps.users.serializers import UserShortSerializer

class ClubEventSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClubEvent
        fields = ['id', 'title', 'description', 'event_date', 'location', 'created_at']

class ClubSerializer(serializers.ModelSerializer):
    president = UserShortSerializer(read_only=True)
    is_member = serializers.SerializerMethodField()
    events = ClubEventSerializer(many=True, read_only=True)

    class Meta:
        model = Club
        fields = ['id', 'name', 'description', 'logo', 'president',
                  'members_count', 'is_active', 'created_at', 'is_member', 'events']

    def get_is_member(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return obj.members.filter(pk=request.user.pk).exists()
        return False