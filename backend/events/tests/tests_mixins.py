from django.test import TestCase
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from rest_framework.exceptions import ValidationError
from rest_framework.test import APIRequestFactory

from events import serializers
from events.models import Location
from users.models import ConcertifyUser


class TestValidateUserInContextMixin(TestCase):
    def setUp(self):
        self.serializer_class = serializers.EventFeedSerializer
        self.factory = APIRequestFactory()
        self.user = ConcertifyUser.objects.create_user(
            username='test',
            password='test'
        )
        location = Location.objects.create(
            name='test',
            address_line='test',
            city='test',
            postal_code='test',
            country='TST'
        )
        self.data = {
            'title': 'test',
            'desc': 'Test test',
            'location': location.id
        }

    def test_validate_GET(self):
        """When calling GET method validation should be performed as usual"""
        request = self.factory.get(reverse('events:event-list'))
        serializer = self.serializer_class(
            context={'request': request},
            data=self.data
        )
        serializer.is_valid(raise_exception=True)

    def test_validate_no_user(self):
        """Calling method different than GET without user in context will """\
            """raise ValidationError"""
        request = self.factory.post(reverse('events:event-list'))
        serializer = self.serializer_class(
            context={'request': request},
            data=self.data
        )

        with self.assertRaises(ValidationError):
            serializer.is_valid(raise_exception=True)
        self.assertIn(
            _("Serializer is missing user in context"),
            list(map(str, serializer.errors['non_field_errors']))
        )

    def test_validate_user(self):
        """Calling method different than GET with user shouldn't"""\
            """ raise anything"""
        request = self.factory.post(reverse('events:event-list'))
        request.user = self.user
        serializer = self.serializer_class(
            context={'request': request},
            data=self.data
        )
        serializer.is_valid(raise_exception=True)
