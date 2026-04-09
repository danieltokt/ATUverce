from rest_framework import generics, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import User, Follow
from .serializers import UserSerializer, UserShortSerializer, RegisterSerializer
from rest_framework.views import APIView
from django.contrib.auth import get_user_model

class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]

class MeView(generics.RetrieveUpdateAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user

class UserDetailView(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def search_users(request):
    q = request.query_params.get('q', '')
    users = User.objects.filter(username__icontains=q)[:10] if q else []
    return Response(UserShortSerializer(users, many=True).data)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def follow_user(request, pk):
    target = get_object_or_404(User, pk=pk)
    if target == request.user:
        return Response({'error': 'Нельзя подписаться на себя'}, status=400)

    follow, created = Follow.objects.get_or_create(follower=request.user, following=target)
    if not created:
        follow.delete()
        target.followers_count = max(0, target.followers_count - 1)
        request.user.following_count = max(0, request.user.following_count - 1)
        action = 'unfollowed'
    else:
        target.followers_count += 1
        request.user.following_count += 1
        action = 'followed'

    target.save()
    request.user.save()
    return Response({'action': action, 'followers_count': target.followers_count})

User = get_user_model()

class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        data = request.data
        username = data.get('username', '').strip()
        password = data.get('password', '')
        email = data.get('email', '').strip()
        first_name = data.get('first_name', '').strip()
        last_name = data.get('last_name', '').strip()
        group = data.get('group', '').strip()
        faculty = data.get('faculty', '').strip()
        year = data.get('year_of_study')

        if not username or not password:
            return Response({'error': 'Логин и пароль обязательны'}, status=400)
        if User.objects.filter(username=username).exists():
            return Response({'error': 'Логин уже занят'}, status=400)

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name,
            group=group,
            faculty=faculty,
            year_of_study=year,
        )
        return Response({'id': user.id, 'username': user.username}, status=201)