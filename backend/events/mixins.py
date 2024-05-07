import copy

from django.utils import timezone

from rest_framework.exceptions import NotAuthenticated, ValidationError

from celery import shared_task
from celery.result import AsyncResult

from events import models
from users import models as users_models


class ValidateUserInContextMixin:
    def validate(self, attrs):
        request = self.context.get("request")

        if request.method != 'GET':
            if not hasattr(request, "user"):
                msg = "Serializer is missing user in context"
                raise ValidationError(msg)

            if not request.user.is_authenticated:
                raise NotAuthenticated()
        return attrs


class CreateNotificationMixin:
    @staticmethod
    def create_notifications_for_users(template, users):
        for user in users:
            notification = copy.deepcopy(template)
            notification.user = user
            notification.save()

    def _schedule_reminder(self, event):
        if not event.start:
            print("Event is missing start date")
            return
        eta = event.start - timezone.timedelta(days=1)
        self.send_reminders.apply_async(
            args=(event.id, event.title, event.start),
            eta=eta,
            task_id=self.generate_task_id(event)
        )

    def revoke_task(self, event):
        try:
            result = AsyncResult(self.generate_task_id(event))
            if result.state in ['PENDING']:
                result.revoke(terminate=False)
        except Exception:
            print("Error while revoking task related with reminder")

    def generate_task_id(self, event):
        return "event: " + str(event.pk)

    @staticmethod
    @shared_task
    def send_reminders(event_id, event_title, start_date):
        users = users_models.ConcertifyUser.objects.filter(
            role__event_id=event_id,
            role__name=models.Role.NameChoice.USER
        )
        template = users_models.Notification(
            title="Reminder about upcoming event",
            desc=f"""The event "{event_title}" starts """
            f"""{start_date.strftime('%Y-%m-%d %H:%M:%S')}""",
            notification_type=users_models.Notification.TypeChoice.REMINDER
        )
        CreateNotificationMixin.create_notifications_for_users(template, users)
