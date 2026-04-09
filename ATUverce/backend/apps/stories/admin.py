from django.contrib import admin
from .models import Story

@admin.register(Story)
class StoryAdmin(admin.ModelAdmin):
    list_display = ['author', 'media_type', 'views_count', 'expires_at', 'created_at']