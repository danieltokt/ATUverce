from django.urls import path
from . import views

urlpatterns = [
    path('chat/', views.ChatAPIView.as_view()),
    path('sessions/', views.SessionListView.as_view()),
    path('sessions/<int:pk>/', views.SessionDetailView.as_view()),
]