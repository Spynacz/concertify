from django.urls import reverse
from django.test import TestCase

from rest_framework.test import APIRequestFactory

from knox.models import AuthToken

from events import serializers
from events.models import Event, Location, Role
from users.models import ConcertifyUser


class TestLocationSerializer(TestCase):
    def setUp(self):
        self.serializer_class = serializers.LocationSerializer
        self.data = {
            'name': 'test',
            'address_line': 'test',
            'city': 'test',
            'postal_code': 'test',
            'country': 'TST'
        }

    def test_create_new(self):
        """When creating not existing object nothing should happen"""
        serializer = self.serializer_class(data=self.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

    def test_create_existing(self):
        """When attempting to create existing object nothing should happen"""
        location = Location.objects.create(**self.data)

        serializer = self.serializer_class(data=self.data)
        serializer.is_valid(raise_exception=True)
        instance = serializer.save()

        self.assertEqual(location, instance)


class TestEventFeedSerializer(TestCase):
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
        self.token = f"Token {AuthToken.objects.create(user=self.user)[-1]}"

    def test_create(self):
        """create method should make an owner role
           for the user that creates it."""
        request = self.factory.get(reverse('events:event-list'))
        request.user = self.user

        serializer = self.serializer_class(
            context={'request': request},
            data=self.data
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()

        role = Role.objects.get(user=self.user)

        self.assertIsNotNone(role)
        self.assertEqual(int(role.name), Role.NameChoice.OWNER)


class TestEventDetailsSerializer(TestCase):
    fixtures = ['fixtures/test_fixture.json']

    def setUp(self):
        self.event = Event.objects.get(id=1)
        self.serializer = serializers.EventDetailsSerializer(
            instance=self.event)

    def test_get_event_contacts(self):
        """Method should return list of EventContact object data"""
        event_contacts = [
            {
                'id': obj.id,
                'name': obj.name,
                'phone': obj.phone
            } for obj in self.event.event_contact.all()
        ]
        self.assertEqual(
            event_contacts,
            self.serializer.data['event_contacts']
        )

    def test_get_social_media(self):
        """Method should return list of SocialMedia object data"""
        social_media = [
            {
                'id': obj.id,
                'link': obj.link,
                'platform': obj.platform
            } for obj in self.event.social_media.all()
        ]
        self.assertEqual(
            social_media,
            self.serializer.data['social_media']
        )

    def test_get_location(self):
        """Method should return Location object data"""
        location = {
                'id': self.event.location.id,
                'name': self.event.location.name,
                'address_line': self.event.location.address_line,
                'postal_code': self.event.location.postal_code,
                'country': self.event.location.country
            }

        self.assertEqual(
            location,
            self.serializer.data['location']
        )
