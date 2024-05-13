from rest_framework import exceptions

from events.models import Role


class VoteMixin:
    def get_vote_count(self, obj):
        return obj.votes.all().count()

    def get_has_voted(self, obj):
        request = self.context.get("request", None)

        if not hasattr(request, "user") or not request.user.is_authenticated:
            return False

        votes = obj.votes.all()
        return votes.filter(user=request.user).exists()


class IsEventModeratorPerformCreateMixin:
    def perform_create(self, serializer):
        event = serializer.validated_data.get('event')

        try:
            role = Role.objects.get(event=event, user=self.request.user)
        except Role.DoesNotExist:
            msg = "You do not have a role in related event."
            raise exceptions.PermissionDenied(msg)

        if int(role.name) < Role.NameChoice.MODERATOR:
            msg = "You do not have permission to perform this action."
            raise exceptions.PermissionDenied(msg)

        return super().perform_create(serializer)
