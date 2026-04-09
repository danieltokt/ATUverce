from django.urls import path
from . import views

urlpatterns = [
    path('', views.ClubListView.as_view(), name='clubs'),
    path('<int:pk>/join/', views.join_club, name='join-club'),
]