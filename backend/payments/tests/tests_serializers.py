import decimal

from django.test import TestCase
from django.urls import reverse

from rest_framework.test import APIRequestFactory

from events.models import Event, Location, Ticket
from payments import serializers
from payments.models import Order
from users.models import ConcertifyUser


class TestCartItemSerializer(TestCase):
    def setUp(self):
        self.serializer_class = serializers.OrderItemSerializer
        self.user = ConcertifyUser.objects.create(
            username="test",
            email='test@email.com',
            password='test'
        )
        location = Location.objects.create(
            name='test',
            address_line='test',
            city='test',
            postal_code='test',
            country='TST'
        )
        self.event = Event.objects.create(
            title='test1',
            desc='Test test1',
            location=location
        )
        self.ticket = Ticket.objects.create(
            title='test',
            desc='test',
            quantity=1000,
            amount=12.01,
            event=self.event
        )
        self.order = Order.objects.create(user=self.user)
        self.data = {
            'ticket_type': '0.5',
            'quantity': 2,
            'ticket': self.ticket.id,
            'order': self.order.id
        }

    def test_get_total_amount(self):
        """Serializer should return total ticket item cost"""
        serializer = self.serializer_class(data=self.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        data = serializer.data

        self.assertEqual(
            data.get('total_amount'),
            round(
                decimal.Decimal(self.ticket.amount)
                * decimal.Decimal(data.get("quantity"))
                * decimal.Decimal(data.get("ticket_type")),
                2
            )
        )

    def test_read_representation(self):
        """Serializer will return more ticket related data when reading"""
        serializer = self.serializer_class(data=self.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        self.data.update(ticket={
            'id': self.ticket.id,
            'title': self.ticket.title,
            'desc': self.ticket.desc,
            'quantity': self.ticket.quantity,
            'amount': decimal.Decimal(str(self.ticket.amount)),
            'event': self.ticket.event.id
        })
        print(self.data, serializer.data)
        self.assertDictContainsSubset(self.data, serializer.data)


class TestCartSerializer(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.serializer_class = serializers.OrderSerializer
        self.user = ConcertifyUser.objects.create(
            username="test",
            email='test@email.com',
            password='test'
        )
        location = Location.objects.create(
            name='test',
            address_line='test',
            city='test',
            postal_code='test',
            country='TST'
        )
        self.event = Event.objects.create(
            title='test1',
            desc='Test test1',
            location=location
        )
        self.ticket = Ticket.objects.create(
            title='test',
            desc='test',
            quantity=1000,
            amount=12.01,
            event=self.event
        )
        self.data = {
            'order_items': [
                {
                    'ticket_type': 0.5,
                    'quantity': 2,
                    'amount': '2.00',
                    'ticket': self.ticket.id
                },
                {
                    'ticket_type': 1,
                    'quantity': 1,
                    'amount': '2.00',
                    'ticket': self.ticket.id
                }
            ]
        }

    def test_get_total(self):
        """get_total should return sum of all ticket items costs"""
        request = self.factory.post(reverse('payments:cart'))
        request.user = self.user
        serializer = self.serializer_class(
            data=self.data,
            context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        print(self.data, serializer.data, serializer.validated_data)
        self.assertEqual(
            serializer.data.get('total'),
            sum([
                round(
                    decimal.Decimal(self.ticket.amount)
                    * decimal.Decimal(item.get("quantity"))
                    * decimal.Decimal(item.get("ticket_type")),
                    2
                )for item in serializer.data.get('order_items')
            ])
        )
