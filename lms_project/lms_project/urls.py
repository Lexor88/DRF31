from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView

urlpatterns = [
    path('admin/', admin.site.urls),

    # Основные API маршруты
    path('api/users/', include('users.urls', namespace='users')),
    path('api/courses/', include('courses.urls', namespace='courses')),
    path('api/payment/', include('payments.urls', namespace='payments')),
    # JWT авторизация
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # DRF UI (Browsable API)
    path('api-auth/', include('rest_framework.urls')),

    # Документация API
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),  # JSON схема API
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),  # Swagger UI
    path('api/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc-ui'),  # ReDoc UI
]
