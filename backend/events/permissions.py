from rest_framework.permissions import BasePermission

from events.models import Role


class EventPermissions(BasePermission):
    def has_permission(self, request, view):
        if view.action in ['list', 'retrieve']:
            return True

        if not request.user.is_authenticated:
            return False

        if view.action == 'create':
            return True

        event = view.kwargs.get('pk')
        if not event:
            return False

        role = Role.objects.get(
            event=event,
            user=request.user
        )

        if view.action == 'delete' and int(role.name) >= Role.NameChoice.OWNER:
            return True
        elif view.action in ['update', 'partial_update']\
                and int(role.name) >= Role.NameChoice.MODERATOR:
            return True
        return False

# Need tweaking
# class IsModerator(BasePermission):
#     def has_permission(self, request, view):
#         if view.action in ['create', 'list', 'retrieve']:
#             return True

#         event = view.kwargs.get('pk')
#         if not event:
#             return False

#         role = Role.objects.get(
#             event=event,
#             user=request.user
#         )

#         if int(role.name) >= Role.NameChoice.MODERATOR:
#             return True
        # return False
