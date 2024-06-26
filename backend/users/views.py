from django.contrib.auth import login

from rest_framework import generics, permissions, viewsets
from rest_framework.permissions import AllowAny, IsAuthenticated

from knox.views import LoginView as KnoxLoginView

from users import serializers
from users import models


class CreateUserViews(generics.CreateAPIView):
    serializer_class = serializers.UserSerializer


class LoginView(KnoxLoginView):
    permission_classes = [AllowAny]

    def post(self, request, format=None):
        serializer = serializers.AuthSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        login(request, user)
        return super(LoginView, self).post(request, format=None)


class PasswordChangeView(generics.UpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = serializers.PasswordSerializer

    def get_object(self):
        return self.request.user


class ManageUserView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = serializers.ManageUserSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user


class UserNotificationView(generics.ListAPIView, generics.UpdateAPIView):
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.request.method == 'PUT':
            return serializers.UserNotificationSetAsSeenSerializer
        return serializers.UserNotificationSerializer

    def get_queryset(self):
        return models.Notification.objects.filter(user=self.request.user)


class EventReportViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.EventReport

    def get_permissions(self):
        if (self.request.method in permissions.SAFE_METHODS
                or self.request.method in ['PUT', 'PATCH']):
            permission_classes = [permissions.IsAdminUser]
        else:
            permission_classes = [
                permissions.IsAuthenticated,
            ]
        return [permission() for permission in permission_classes]
