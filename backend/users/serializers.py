from django.contrib.auth import authenticate
from django.utils.translation import gettext_lazy as _

from rest_framework import serializers

from users.models import ConcertifyUser, PaymentInfo


class PaymentInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentInfo
        fields = '__all__'
        extra_kwargs = {'user': {'required': False}}


class UserSerializer(serializers.ModelSerializer):
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
        payment_info = validated_data.pop('payment_info')
        payment_info.update({'user': instance})

        PaymentInfoSerializer().update(payment_instance, payment_info)

        return super().update(instance, validated_data)


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
            msg = _('Unable to log in with provided credentials.')
            raise serializers.ValidationError(msg, code='authentication')

        attrs['user'] = user
        return attrs
