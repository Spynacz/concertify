from django.db import models
from django.utils.translation import gettext_lazy as _


class Event(models.Model):
    title = models.CharField(_("title"), max_length=150)
    desc = models.CharField(_("description"), max_length=300)
    picture = models.ImageField()


class Role(models.Model):
    class NameChoice(models.TextChoices):
        OWNER = ('OWNER', _('owner'))
        MODERATOR = ('MODERATOR', _('moderator'))
        STAFF = ('STAFF', _('staff'))
        USER = ('USER', _('user'))

    event = models.ForeignKey(Event, related_name="role",
                              on_delete=models.CASCADE)
    user = models.ForeignKey('users.ConcertifyUser', related_name="role",
                             on_delete=models.CASCADE)
    name = models.CharField(_('role name'))

    class Meta:
        unique_together = [['event', 'user']]
