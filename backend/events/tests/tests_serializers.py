from django.urls import reverse
from django.test import TestCase

from rest_framework.test import APIRequestFactory

from knox.models import AuthToken

from events.models import Location, Role
from events.serializers import EventSerializer
from users.models import ConcertifyUser


class TestEventSerializer(TestCase):
    def setUp(self):
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
        self.token = f"Token {AuthToken.objects.create(user=self.user)[-1]}"

    def test_create(self):
        """create method should make an owner role
           for the user that creates it."""
        request = self.factory.get(reverse('events:event-list'))
        request.user = self.user

        serializer = EventSerializer(
            context={'request': request},
            data=self.data
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()

        role = Role.objects.get(user=self.user)

        self.assertIsNotNone(role)
        self.assertEqual(int(role.name), Role.NameChoice.OWNER)
