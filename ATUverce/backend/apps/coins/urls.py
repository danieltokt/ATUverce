from django.urls import path
from . import views

urlpatterns = [
    path('my/', views.my_coins, name='my-coins'),
    path('leaderboard/', views.leaderboard, name='leaderboard'),
]