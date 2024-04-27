from django.contrib.auth import authenticate
from django.contrib.auth.hashers import check_password
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError as DjangoValidationError

from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from events.serializers import ValidateUserInContextMixin
from users.models import ConcertifyUser, PaymentInfo, Notification


class ValidatePasswordMixin:
    def validate_password(self, password):
        try:
            validate_password(password)
        except DjangoValidationError as e:
            raise ValidationError(e.messages)
        return password


class PaymentInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentInfo
        fields = '__all__'
        extra_kwargs = {'user': {'read_only': True}}


class UserSerializer(ValidatePasswordMixin,
                     serializers.ModelSerializer):
    payment_info = PaymentInfoSerializer(required=False)

    class Meta:
        model = ConcertifyUser
        fields = [
            'first_name',
            'last_name',
            'username',
            'email',
            'password',
            'payment_info'
        ]
        extra_kwargs = {
            'password': {'write_only': True, 'min_length': 9}}

    def create(self, validated_data):
        payment_info = validated_data.pop('payment_info', None)
        user = ConcertifyUser.objects.create_user(**validated_data)

        if payment_info:
            payment_info.update({'user': user})
        else:
            payment_info = {'user': user}
        PaymentInfo.objects.create(**payment_info)

        return user

    def update(self, instance, validated_data):
        payment_instance = instance.payment_info
        payment_info = validated_data.pop('payment_info', None)
        if payment_info:
            payment_info.update({'user': instance})
            PaymentInfoSerializer().update(payment_instance, payment_info)

        return super().update(instance, validated_data)


class ManageUserSerializer(UserSerializer):
    class Meta:
        model = ConcertifyUser
        fields = [
            'first_name',
            'last_name',
            'username',
            'email',
            'payment_info'
        ]


class PasswordSerializer(ValidatePasswordMixin,
                         ValidateUserInContextMixin,
                         serializers.Serializer):
    old_password = serializers.CharField(max_length=128, write_only=True)
    password1 = serializers.CharField(max_length=128, write_only=True)
    password2 = serializers.CharField(max_length=128, write_only=True)

    def validate_old_password(self, old_password):
        user = self.context.get('request').user

        if not check_password(old_password, user.password):
            raise ValidationError("Current password is incorrect")

    def validate_password1(self, password1):
        return super().validate_password(password1)

    def validate(self, attrs):
        attrs = super().validate(attrs)

        password1 = attrs['password1']
        password2 = attrs['password2']

        if password1 != password2:
            msg = {
                'password1': "New passwords are not the same",
                'password2': "New passwords are not the same"
            }
            raise ValidationError(msg)

        return attrs

    def update(self, instance, validated_data):
        instance.set_password(validated_data['password1'])
        instance.save()
        return instance


class AuthSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(
        style={'input_style': 'password'},
        trim_whitespace=False
    )

    def validate(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')

        user = authenticate(
            request=self.context.get('request'),
            username=username,
            password=password
        )

        if not user:
            msg = 'Unable to log in with provided credentials.'
            raise serializers.ValidationError(msg, code='authentication')

        attrs['user'] = user
        return attrs

class UserNotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model =  Notification
        fields = ['title',
                  'desc',
                  'notification_type',
                  'has_been_seen']
        
class UserNotificationSetAsSeenSerializer(serializers.ModelSerializer):

    class Meta:
        model = Notification
        fields = []

    def update(self, instance, validated_data):
        instance.has_been_seen = True
        instance.save()
        return instance