from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.decorators import action
from django.contrib.auth import get_user_model
from .serializers import UserSerializer
from .permissions import IsUserOrReadOnly, IsModeratorReadOnly

User = get_user_model()

class UserViewSet(viewsets.ModelViewSet):
    """
    ViewSet для пользователей:
    - Пользователи могут редактировать только свой профиль.
    - Модераторы могут просматривать и редактировать всех пользователей, но не удалять.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated, IsUserOrReadOnly | IsModeratorReadOnly]

    def get_permissions(self):
        if self.action in ["create", "register"]:
            return [AllowAny()]
        return super().get_permissions()

    @action(detail=False, methods=['post'], permission_classes=[AllowAny])
    def register(self, request):
        """Регистрация нового пользователя с корректным хешированием пароля"""
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            user.set_password(serializer.validated_data['password'])
            user.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
