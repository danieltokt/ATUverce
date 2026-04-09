from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Follow

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ['username', 'get_full_name', 'faculty', 'role', 'ala_coins', 'is_verified']
    list_filter = ['role', 'faculty', 'is_verified']
    search_fields = ['username', 'first_name', 'last_name', 'email']
    fieldsets = UserAdmin.fieldsets + (
        ('ATUverce', {'fields': ('avatar', 'bio', 'role', 'group', 'faculty', 'year_of_study', 'skills', 'interests', 'github', 'linkedin', 'portfolio', 'ala_coins', 'is_verified')}),
    )

@admin.register(Follow)
class FollowAdmin(admin.ModelAdmin):
    list_display = ['follower', 'following', 'created_at']