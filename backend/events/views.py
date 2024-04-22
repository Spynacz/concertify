from django.utils import timezone

from rest_framework import mixins, permissions, viewsets

from events import permissions as event_permissions
from events import models, serializers


class LocationViewSet(mixins.ListModelMixin,
                      mixins.CreateModelMixin,
                      viewsets.GenericViewSet):
    serializer_class = serializers.LocationSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        return models.Location.objects.all()


class EventViewSet(viewsets.ModelViewSet):
    def get_queryset(self):
        if self.action == 'list':
            return models.Event.objects.filter(end__gt=timezone.now())
        return models.Event.objects.all()

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return serializers.EventDetailsSerializer
        return serializers.EventFeedSerializer

    def get_permissions(self):
        if self.request.method in permissions.SAFE_METHODS:
            permission_classes = [permissions.AllowAny]
        elif self.action == 'create':
            permission_classes = [permissions.IsAuthenticated]
        elif self.action in ['update', 'partial_update']:
            permission_classes = [
                permissions.IsAuthenticated,
                event_permissions.IsEventModerator
            ]
        else:  # destroy
            permission_classes = [
                permissions.IsAuthenticated,
                event_permissions.IsEventOwner
            ]
        return [permission() for permission in permission_classes]


class RoleViewSet(mixins.CreateModelMixin,
                  mixins.DestroyModelMixin,
                  mixins.UpdateModelMixin,
                  viewsets.GenericViewSet):
    serializer_class = serializers.RoleSerializer

    def get_queryset(self):
        return models.Role.objects.all()

    def get_permissions(self):
        if self.action == 'create':
            permission_classes = [permissions.IsAuthenticated]
        elif self.action == 'destroy':
            permission_classes = [
                permissions.IsAuthenticated,
                event_permissions.DestroyRolePermission
            ]
        else:  # update, partial_update
            permission_classes = [
                permissions.IsAuthenticated,
                event_permissions.IsEventOwner
            ]
        return [permission() for permission in permission_classes]


class EventContactViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.EventContactSerializer
    permission_classes = [
        permissions.IsAuthenticated,
        event_permissions.IsEventModerator
    ]

    def get_queryset(self):
        return models.EventContact.objects.all()


class SocialMediaViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.SocialMediaSerializer
    permission_classes = [
        permissions.IsAuthenticated,
        event_permissions.IsEventModerator
    ]

    def get_queryset(self):
        return models.SocialMedia.objects.all()


class TicketViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.SocialMediaSerializer
    permission_classes = [
        permissions.IsAuthenticated,
        event_permissions.IsEventOwner
    ]

    def get_queryset(self):
        return models.Ticket.objects.all()
