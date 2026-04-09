from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from apps.users.models import User
from .models import CoinTransaction

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def my_coins(request):
    transactions = CoinTransaction.objects.filter(user=request.user)[:20]
    data = [{
        'id': t.id,
        'amount': t.amount,
        'reason': t.get_reason_display(),
        'description': t.description,
        'created_at': t.created_at,
    } for t in transactions]
    return Response({'total': request.user.ala_coins, 'transactions': data})

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def leaderboard(request):
    users = User.objects.order_by('-ala_coins')[:50]
    data = [{
        'id': u.id,
        'username': u.username,
        'full_name': u.get_full_name() or u.username,
        'avatar': u.avatar.url if u.avatar else None,
        'faculty': u.faculty,
        'ala_coins': u.ala_coins,
    } for u in users]
    return Response(data)