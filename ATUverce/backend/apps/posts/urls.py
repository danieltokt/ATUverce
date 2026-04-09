from django.urls import path
from . import views

urlpatterns = [
    path('', views.FeedView.as_view(), name='posts'),
    path('<int:pk>/', views.PostDetailView.as_view(), name='post-detail'),
    path('<int:pk>/like/', views.like_post, name='like-post'),
    path('<int:pk>/comments/', views.post_comments, name='post-comments'),
]