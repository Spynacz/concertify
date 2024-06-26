from rest_framework.permissions import BasePermission

from events.models import Role, Event


class IsEventModerator(BasePermission):
    # View permissions ?
    def has_object_permission(self, request, view, obj):
        if isinstance(obj, Event):
            event = obj
        else:
            event = obj.event

        try:
            role = Role.objects.get(event=event, user=request.user)
        except Role.DoesNotExist:
            return False

        if int(role.name) >= Role.NameChoice.MODERATOR:
            return True
        return False


class IsEventOwner(BasePermission):
    # View permissions ?
    def has_object_permission(self, request, view, obj):
        if isinstance(obj, Event):
            event = obj
        else:
            event = obj.event

        try:
            role = Role.objects.get(event=event, user=request.user)
        except Role.DoesNotExist:
            return False

        if int(role.name) >= Role.NameChoice.OWNER:
            return True
        return False


class DestroyRolePermission(BasePermission):
    def has_object_permission(self, request, view, obj):
        event = obj.event

        try:
            role = Role.objects.get(event=event, user=request.user)
        except Role.DoesNotExist:
            return False

        if int(role.name) == Role.NameChoice.OWNER:
            return True
        if request.user == obj.user:
            return True
        return False


class CreateNotificiationPermision(BasePermission):
    def has_permission(self, request, view):
        pk = view.kwargs.get('pk')
        try:
            role = Role.objects.get(event_id=pk, user=request.user)
        except Role.DoesNotExist:
            return False

        if int(role.name) >= Role.NameChoice.MODERATOR:
            return True
        return False
