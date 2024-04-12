from django.contrib.auth import authenticate
from django.utils.translation import gettext_lazy as _

from rest_framework import serializers

from users.models import ConcertifyUser


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = ConcertifyUser
        fields = [
            'first_name',
            'last_name',
            'username',
            'email',
            'password'
        ]
        extra_kwargs = {'password': {'write_only': True, 'min_length': 9}}

    def create(self, validated_data):
        user = ConcertifyUser.objects.create_user(**validated_data)
        return user


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