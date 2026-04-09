from rest_framework import generics, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import Post, Like, Comment
from .serializers import PostSerializer, CommentSerializer
from apps.coins.utils import award_coins

class FeedView(generics.ListCreateAPIView):
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Post.objects.select_related('author').all()

    def perform_create(self, serializer):
        post = serializer.save(author=self.request.user)
        award_coins(self.request.user, 'post_created', f'Создал пост #{post.id}')

class PostDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        obj = super().get_object()
        obj.views_count += 1
        obj.save(update_fields=['views_count'])
        return obj

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def like_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    like, created = Like.objects.get_or_create(user=request.user, post=post)
    if not created:
        like.delete()
        post.likes_count = max(0, post.likes_count - 1)
    else:
        post.likes_count += 1
        award_coins(request.user, 'activity', f'Лайк на пост #{post.id}')
    post.save(update_fields=['likes_count'])
    return Response({'likes_count': post.likes_count, 'is_liked': created})

@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def post_comments(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == 'GET':
        comments = post.comments.select_related('author').filter(parent=None)
        return Response(CommentSerializer(comments, many=True).data)
    serializer = CommentSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(author=request.user, post=post)
        post.comments_count += 1
        post.save(update_fields=['comments_count'])
        award_coins(request.user, 'comment', f'Комментарий к посту #{post.id}')
        return Response(serializer.data, status=201)
    return Response(serializer.errors, status=400)