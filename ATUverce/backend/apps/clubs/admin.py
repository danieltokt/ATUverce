from django.contrib import admin
from .models import Club, ClubEvent

@admin.register(Club)
class ClubAdmin(admin.ModelAdmin):
    list_display = ['name', 'president', 'members_count', 'is_active']
    list_filter = ['is_active']

@admin.register(ClubEvent)
class ClubEventAdmin(admin.ModelAdmin):
    list_display = ['title', 'club', 'event_date']