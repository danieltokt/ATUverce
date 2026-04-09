from django.contrib import admin
from .models import Post, Like, Comment

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['author', 'post_type', 'likes_count', 'comments_count', 'created_at']
    list_filter = ['post_type']
    search_fields = ['author__username', 'content']

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['author', 'post', 'created_at']

admin.site.register(Like)