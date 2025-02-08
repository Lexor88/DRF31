from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('admin/', admin.site.urls),


    # Основные API маршруты
    path('api/users/', include('users.urls', namespace='users')),
    path('api/courses/', include('courses.urls', namespace='courses')),

    # JWT авторизация
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # DRF UI (Browsable API)
    path('api-auth/', include('rest_framework.urls')),
]
