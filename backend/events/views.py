from django.core.cache import cache
from django.utils import timezone

from rest_framework import exceptions, mixins, permissions, status, viewsets, generics
from rest_framework.filters import SearchFilter
from rest_framework.response import Response
from rest_framework.views import APIView

from events import permissions as event_permissions
from events import models, serializers
from posts_comments.views import IsEventModeratorPerformCreateMixin


class LocationViewSet(mixins.ListModelMixin,
                      mixins.CreateModelMixin,
                      viewsets.GenericViewSet):
    serializer_class = serializers.LocationSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        return models.Location.objects.all()


class EventViewSet(viewsets.ModelViewSet):
    filter_backends = [SearchFilter]
    search_fields = [
        'title',
        'location__name',
        '^location__city',
        '^location__country'
    ]

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

    def perform_destroy(self, instance):
        serializers.EventFeedSerializer.revoke_task(instance)
        super().perform_destroy(instance)


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


class EventContactViewSet(IsEventModeratorPerformCreateMixin,
                          viewsets.ModelViewSet):
    serializer_class = serializers.EventContactSerializer
    permission_classes = [
        permissions.IsAuthenticated,
        event_permissions.IsEventModerator
    ]

    def get_queryset(self):
        return models.EventContact.objects.all()


class SocialMediaViewSet(IsEventModeratorPerformCreateMixin,
                         viewsets.ModelViewSet):
    serializer_class = serializers.SocialMediaSerializer
    permission_classes = [
        permissions.IsAuthenticated,
        event_permissions.IsEventModerator
    ]

    def get_queryset(self):
        return models.SocialMedia.objects.all()


class SchedulItemViewSet(IsEventModeratorPerformCreateMixin,
                         viewsets.ModelViewSet):
    serializer_class = serializers.SocialMediaSerializer
    permission_classes = [
        permissions.IsAuthenticated,
        event_permissions.IsEventModerator
    ]

    def get_queryset(self):
        return models.ScheduleItem.objects.all()


class TicketViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.SocialMediaSerializer
    permission_classes = [
        permissions.IsAuthenticated,
        event_permissions.IsEventOwner
    ]

    def get_queryset(self):
        return models.Ticket.objects.all()

    def perform_create(self, serializer):
        event = serializer.validated_data.get('event')

        try:
            role = models.Role.objects.get(event=event, user=self.request.user)
        except models.Role.DoesNotExist:
            msg = "You do not have a role in related event."
            raise exceptions.PermissionDenied(msg)

        if int(role.name) < models.Role.NameChoice.OWNER:
            msg = "You do not have permission to perform this action."
            raise exceptions.PermissionDenied(msg)

        return super().perform_create(serializer)


class ShoppingCartView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get_cart(self, id):
        data = cache.get(id)
        if not data:
            return Response({'error': 'No data assigned to the given key.'},
                            status=status.HTTP_400_BAD_REQUEST)
        return data

    def get(self, request, *args, **kwargs):
        data = self.get_cart(request.user.id)
        if isinstance(data, Response):
            return data

        serializer = serializers.CartSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        serializer = serializers.CartSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        cache.set(request.user.id, serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def put(self, request, *args, **kwargs):
        serializer = serializers.CartSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        old_data = cache.get(request.user.id)
        cache.set(request.user.id, serializer.data)

        if old_data:
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def delete(self, request, *args, **kwargs):
        cache.delete(request.user.id)
        return Response(status=status.HTTP_204_NO_CONTENT)


class CreateNotificationView(generics.CreateAPIView):
    serializer_class = serializers.NotificationSerializer
    permission_classes = [
        permissions.IsAuthenticated,
        event_permissions.CreateNotificiationPermision
    ]
