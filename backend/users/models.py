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
    telephone = PhoneNumberField(blank=True, null=True)
    mobile = PhoneNumberField(blank=True, null=True)
    user = models.OneToOneField(
        ConcertifyUser, related_name='payment_info', on_delete=models.CASCADE
    )
