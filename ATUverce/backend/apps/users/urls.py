from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.RegisterView.as_view(), name='register'),
    path('me/', views.MeView.as_view(), name='me'),
    path('search/', views.search_users, name='search-users'),
    path('<int:pk>/', views.UserDetailView.as_view(), name='user-detail'),
    path('<int:pk>/follow/', views.follow_user, name='follow-user'),
]