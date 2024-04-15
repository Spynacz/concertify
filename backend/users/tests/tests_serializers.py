from django.contrib.auth.hashers import check_password, make_password
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.test import TestCase

from rest_framework.test import APIRequestFactory
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


class TestPasswordSerializer(TestCase):
    def setUp(self):
        self.serializer_class = serializers.PasswordSerializer
        self.old_password = "TestTest123"
        self.user = ConcertifyUser.objects.create(
            username="test",
            email="test@email.com",
            password=make_password(self.old_password)
        )
        factory = APIRequestFactory()
        url = reverse("users:password-change")
        self.request = factory.put(url)
        self.request.user = self.user

    def test_validate_incorrect_old_password(self):
        """When given incorrect old_password Validation Error will be raised"""
        data = {
            'old_password': 'incorrect',
            'password1': 'new_password123',
            'password2': 'new_password123',
        }
        serializer = self.serializer_class(
            instance=self.user,
            data=data,
            context={'request': self.request}
        )
        with self.assertRaises(ValidationError):
            serializer.is_valid(raise_exception=True)
        self.assertIn(
            _("Current password is incorrect"),
            list(map(str, serializer.errors['old_password']))
        )

    def test_validate_new_paswords_dont_match(self):
        """When password 1 and 2 don't match Validation Error will be raised"""
        data = {
            'old_password': self.old_password,
            'password1': 'incorrect',
            'password2': 'new_password123',
        }
        serializer = self.serializer_class(
            instance=self.user,
            data=data,
            context={'request': self.request}
        )

        with self.assertRaises(ValidationError):
            serializer.is_valid(raise_exception=True)
        self.assertIn(
            _("New passwords are not the same"),
            list(map(str, serializer.errors['non_field_errors']))
        )

    def test_update_valid(self):
        """When given valid data password will be updated"""
        new_password = '123'
        data = {
            'old_password': self.old_password,
            'password1': new_password,
            'password2': new_password,
        }
        serializer = self.serializer_class(
            instance=self.user,
            data=data,
            context={'request': self.request}
        )

        serializer.is_valid(raise_exception=True)
        serializer.save()
        self.assertTrue(check_password(new_password, self.user.password))
