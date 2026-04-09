from rest_framework import serializers
from .models import Post, Comment, Like
from apps.users.serializers import UserShortSerializer

class CommentSerializer(serializers.ModelSerializer):
    author = UserShortSerializer(read_only=True)

    class Meta:
        model = Comment
        fields = ['id', 'author', 'content', 'created_at', 'parent']
        read_only_fields = ['author']

class PostSerializer(serializers.ModelSerializer):
    author = UserShortSerializer(read_only=True)
    is_liked = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = [
            'id', 'author', 'content', 'post_type', 'media',
            'tags', 'likes_count', 'comments_count', 'views_count',
            'is_pinned', 'created_at', 'is_liked'
        ]
        read_only_fields = ['author', 'likes_count', 'comments_count', 'views_count']

    def get_is_liked(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return Like.objects.filter(user=request.user, post=obj).exists()
        return False