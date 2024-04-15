from django.utils.translation import gettext_lazy as _
from django.test import TestCase

from rest_framework.serializers import ValidationError

from users import serializers
from users.models import ConcertifyUser


class TestUserSerializer(TestCase):
    def setUp(self):
        self.u_serializer = serializers.UserSerializer
        self.pi_serializer = serializers.PaymentInfoSerializer
        self.data = {
            'username': 'test',
            'email': 'test@email.com',
            'password': 'TestTest123',
            'payment_info': {
                'line1': 'test',
                'line2': 'test',
                'city': 'Test',
                'postal_code': '12-345',
                'country': 'TST',
                'telephone': '+48893742097',
                'mobile': '+48893742097'
            }
        }

    def test_create_method_no_payment_info(self):
        """create method chould create new user and empty PaymentInfo"""
        self.data.pop('payment_info')
        serializer = self.u_serializer(data=self.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        user = ConcertifyUser.objects.get(username=self.data['username'])
        self.assertIsNotNone(user)
        self.assertIsNotNone(user.payment_info)

    def test_create_method_payment_info(self):
        """create method chould create new user and PaymentInfo if given"""
        serializer = self.u_serializer(data=self.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        user = ConcertifyUser.objects.get(username=self.data['username'])
        self.assertIsNotNone(user)
        self.assertIsNotNone(user.payment_info)

    def test_update_method_no_payment_info(self):
        """User can be updated without affecting payment_info"""
        serializer = self.u_serializer(data=self.data)
        serializer.is_valid(raise_exception=True)
        instance = serializer.save()

        new_data = serializer.validated_data
        payment_info = new_data.pop('payment_info')
        payment_info.pop('user')

        new_data.update({'username': 'new_username'})
        serializer = self.u_serializer(instance=instance, data=new_data)
        serializer.is_valid(raise_exception=True)
        instance = serializer.save()

        serializer = self.pi_serializer(instance=instance.payment_info)

        serializer_data = serializer.data
        serializer_data.pop('user')
        serializer_data.pop('id')

        self.assertDictEqual(dict(payment_info), serializer_data)

    def test_update_method_payment_info(self):
        """payment_info can be updated with user"""
        serializer = self.u_serializer(data=self.data)
        serializer.is_valid(raise_exception=True)
        instance = serializer.save()

        new_data = serializer.validated_data
        new_data['payment_info'].update({'line1': 'new_address'})
        new_data.update({'username': 'new_username'})
        user = new_data['payment_info'].pop('user')

        serializer = self.u_serializer(instance=instance, data=new_data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        new_data['payment_info'].update({'user': user})

        self.assertDictEqual(new_data, serializer.validated_data)

    def test_password_field_is_write_only(self):
        """Password field should be write only."""
        serializer = self.u_serializer(data=self.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        with self.assertRaises(KeyError):
            serializer.data['password']


class TestAuthSerializer(TestCase):
    def setUp(self):
        self.serializer_class = serializers.AuthSerializer
        self.data = {
            'username': 'test',
            'password': 'test'
        }
        self.user = ConcertifyUser.objects.create_user(**self.data)

    def test_validate_valid_data(self):
        """Given valid data validate method should authenticate user."""
        serializer = self.serializer_class(data=self.data)
        serializer.is_valid(raise_exception=True)
        self.assertEqual(self.user, serializer.validated_data['user'])

    def test_validate_invalid_data(self):
        """Given invalid data validdate method should raise ValidationError."""
        serializer = self.serializer_class(data={
            'username': 'invalid',
            'password': 'invalid'
        })
        with self.assertRaises(ValidationError):
            serializer.is_valid(raise_exception=True)
        self.assertEqual(
            str(serializer.errors['non_field_errors'][0]),
            _('Unable to log in with provided credentials.')
        )
