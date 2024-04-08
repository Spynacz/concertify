from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _

from phonenumber_field.modelfields import PhoneNumberField


class ConcertifyUser(AbstractUser):
    email = models.EmailField(_("email address"), unique=True)
    picture = models.ImageField(blank=True, null=True)

    def get_name(self):
        if self.first_name and self.last_name:
            return f"{self.first_name} {self.last_name}"


class PaymentInfo(models.Model):
    line1 = models.CharField(
        _('address line 1'), max_length=300, blank=True, null=True
    )
    line2 = models.CharField(
        _('address line 2'), max_length=300, blank=True, null=True
    )
    city = models.CharField(_('city'), max_length=150, blank=True, null=True)
    postal_code = models.CharField(
        _('postal code'), max_length=20, blank=True, null=True
    )
    country = models.CharField(
        _('country'), max_length=3, blank=True, null=True
    )
    telephone = PhoneNumberField(_('telephone number'), blank=True, null=True)
    mobile = PhoneNumberField(_('mobile phone number'), blank=True, null=True)
    user = models.OneToOneField(
        ConcertifyUser, related_name='payment_info', on_delete=models.CASCADE
    )


class Notification(models.Model):
    title = models.CharField(_('title'), max_length=150)
    desc = models.CharField(_('description'), max_length=300)
    notification_type = models.CharField(
        _('notification type'),
        max_length=100
    )
    user = models.ForeignKey(ConcertifyUser, related_name='notification',
                             on_delete=models.CASCADE)


class EventReport(models.Model):
    title = models.CharField(_('title'), max_length=150)
    desc = models.CharField(_('description'), max_length=300)
    report_type = models.CharField(
        _('report type'),
        max_length=100
    )
    created_at = models.DateTimeField(_('created at'), auto_now_add=True)
    event = models.ForeignKey('events.Event', related_name='report',
                              on_delete=models.DO_NOTHING)
    user = models.ForeignKey(ConcertifyUser, related_name='report',
                             on_delete=models.DO_NOTHING)
