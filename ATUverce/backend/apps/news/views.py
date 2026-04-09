from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .models import News
from .serializers import NewsSerializer

class NewsListView(generics.ListCreateAPIView):
    serializer_class = NewsSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        qs = News.objects.filter(is_published=True)
        category = self.request.query_params.get('category')
        if category:
            qs = qs.filter(category=category)
        return qs

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

class NewsDetailView(generics.RetrieveAPIView):
    queryset = News.objects.filter(is_published=True)
    serializer_class = NewsSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        obj = super().get_object()
        obj.views_count += 1
        obj.save(update_fields=['views_count'])
        return obj