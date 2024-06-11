from django.db import models
from django.utils.translation import gettext_lazy as _

from phonenumber_field.modelfields import PhoneNumberField


class Location(models.Model):
    name = models.CharField(_('location name'), max_length=150)
    address_line = models.CharField(_('address line'), max_length=300)
    city = models.CharField(_('city'), max_length=100)
    postal_code = models.CharField(_('postal code'), max_length=20)
    country = models.CharField(_('country'), max_length=3)


class Event(models.Model):
    title = models.CharField(_('title'), max_length=150)
    desc = models.CharField(_('description'), max_length=300)
    picture = models.URLField(_('picture'), blank=True, null=True)
    start = models.DateTimeField(_('start date'), blank=True, null=True)
    end = models.DateTimeField(_('end date'), blank=True, null=True)
    location = models.ForeignKey(Location, related_name='event',
                                 on_delete=models.DO_NOTHING)


class Role(models.Model):
    class NameChoice(models.IntegerChoices):
        OWNER = (3, _('owner'))
        MODERATOR = (2, _('moderator'))
        STAFF = (1, _('staff'))
        USER = (0, _('user'))

    event = models.ForeignKey(Event, related_name="role",
                              on_delete=models.CASCADE)
    user = models.ForeignKey('users.ConcertifyUser', related_name="role",
                             on_delete=models.CASCADE)
    name = models.CharField(_('role name'), choices=NameChoice.choices)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['event', 'user'], name='unique_event_user_combination'
            )
        ]


class EventContact(models.Model):
    name = models.CharField(_('name'), max_length=200)
    phone = PhoneNumberField(_('phone number'))
    event = models.ForeignKey(Event, related_name="event_contact",
                              on_delete=models.CASCADE)


class SocialMedia(models.Model):
    class PlatformChoice(models.TextChoices):
        X = ('X', 'x')
        INSTAGRAM = ('INSTAGRAM', 'instagram')
        FACEBOOK = ('FACEBOOK', 'facebook')

    link = models.URLField(_('social media link'))
    platform = models.CharField(_('social media platform'),
                                choices=PlatformChoice.choices)
    event = models.ForeignKey(Event, related_name='social_media',
                              on_delete=models.CASCADE)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['event', 'link'], name='unique_event_link_combination'
            )
        ]


class ScheduleItem(models.Model):
    title = models.CharField(_('title'), max_length=150)
    desc = models.CharField(_('description'), max_length=300)
    place = models.CharField(_('place'), max_length=150)
    when = models.DateTimeField(_('when it will happen'))
    event = models.ForeignKey(Event, related_name='schedule',
                              on_delete=models.CASCADE)


class Ticket(models.Model):
    title = models.CharField(_('title'), max_length=150)
    desc = models.CharField(_('description'), max_length=300)
    quantity = models.IntegerField(_('quantity'))
    amount = models.DecimalField(_('amount'), max_digits=9, decimal_places=2)
    event = models.ForeignKey(Event, related_name='ticket',
                              on_delete=models.CASCADE)
