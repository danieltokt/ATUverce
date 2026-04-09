from rest_framework import generics
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import Club
from .serializers import ClubSerializer
from apps.coins.utils import award_coins

class ClubListView(generics.ListAPIView):
    queryset = Club.objects.filter(is_active=True)
    serializer_class = ClubSerializer
    permission_classes = [IsAuthenticated]

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def join_club(request, pk):
    club = get_object_or_404(Club, pk=pk)
    if club.members.filter(pk=request.user.pk).exists():
        club.members.remove(request.user)
        club.members_count = max(0, club.members_count - 1)
        action = 'left'
    else:
        club.members.add(request.user)
        club.members_count += 1
        award_coins(request.user, 'club_participation', f'Вступил в клуб {club.name}')
        action = 'joined'
    club.save(update_fields=['members_count'])
    return Response({'action': action, 'members_count': club.members_count})