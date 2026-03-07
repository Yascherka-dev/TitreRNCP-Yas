from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/auth/', include('apps.users.urls')),
    path('api/auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/matches/', include('apps.matches.urls')),
    path('api/recipes/', include('apps.recipes.urls')),
    path('api/suggestions/', include('apps.suggestions.urls')),
    path('api/favorites/', include('apps.favorites.urls')),
    path('api/comments/', include('apps.comments.urls')),
    path('api/ratings/', include('apps.ratings.urls')),
]
