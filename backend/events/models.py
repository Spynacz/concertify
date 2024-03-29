from django.db import models
from django.utils.translation import gettext_lazy as _

from phonenumber_field.modelfields import PhoneNumberField


class Event(models.Model):
    title = models.CharField(_("title"), max_length=150)
    desc = models.CharField(_("description"), max_length=300)
    picture = models.ImageField(blank=True, null=True)


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
        unique_together = [['event', 'user']]


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
        unique_together = [['link', 'event']]
