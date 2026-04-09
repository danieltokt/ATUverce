from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/users/', include('apps.users.urls')),
    path('api/posts/', include('apps.posts.urls')),
    path('api/stories/', include('apps.stories.urls')),
    path('api/news/', include('apps.news.urls')),
    path('api/clubs/', include('apps.clubs.urls')),
    path('api/coins/', include('apps.coins.urls')),
    path('api/ai/', include('apps.ai_chat.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)