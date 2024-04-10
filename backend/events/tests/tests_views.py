from django.urls import reverse
from django.utils.timezone import now, timedelta

from rest_framework import status
from rest_framework.test import APITestCase

from events.models import Event, Location
from events.serializers import EventDetailsSerializer, EventFeedSerializer


class TestEventViewSet(APITestCase):
    def setUp(self):
        location = Location.objects.create(
            name="test",
            address_line="test",
            city="test",
            postal_code="12-345",
            country="TST"
        )
        self.filtered_out = Event.objects.create(
            title="test1",
            desc="test1",
            start=now() - timedelta(days=20),
            end=now() - timedelta(days=10),
            location=location
        )
        self.in_feed = Event.objects.create(
            title="test2",
            desc="test2",
            start=now() - timedelta(days=20),
            end=now() + timedelta(days=10),
            location=location
        )
        self.url = reverse('events:event-list')

    def test_get_queryset(self):
        "get_queryset should return filtered list of events"
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 1)
        self.assertEqual(
            response.data['results'][0],
            EventFeedSerializer(instance=self.in_feed).data
        )

    def test_serializer_class_retrieve(self):
        """When using retrieve action data should be serialized
           using EventDetailsSerializer"""
        response = self.client.get(
            reverse('events:event-detail', kwargs={'pk': self.filtered_out.id})
        )
        serializer = EventDetailsSerializer(instance=self.filtered_out)

        self.assertEqual(serializer.data, response.data)

    def test_serializer_class_other(self):
        """When using other actions data should be serialized
           using EventFeedSerializer"""
        response = self.client.get(self.url)
        serializer = EventFeedSerializer(instance=self.in_feed)

        self.assertEqual(serializer.data, response.data['results'][0])
