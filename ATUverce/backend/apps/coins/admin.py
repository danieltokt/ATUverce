from django.contrib import admin
from .models import CoinTransaction

@admin.register(CoinTransaction)
class CoinTransactionAdmin(admin.ModelAdmin):
    list_display = ['user', 'amount', 'reason', 'created_at']
    list_filter = ['reason']
    search_fields = ['user__username']