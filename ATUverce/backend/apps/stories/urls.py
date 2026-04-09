from django.urls import path
from . import views

urlpatterns = [
    path('', views.StoryListView.as_view(), name='stories'),
]