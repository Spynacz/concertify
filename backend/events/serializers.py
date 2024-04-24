from rest_framework import serializers
from rest_framework.exceptions import NotAuthenticated, ValidationError

from events import models


class ValidateUserInContextMixin:
    def validate(self, attrs):
        request = self.context.get("request")

        if request.method != 'GET':
            if not hasattr(request, "user"):
                msg = "Serializer is missing user in context"
                raise ValidationError(msg)

            if not request.user.is_authenticated:
                raise NotAuthenticated()
        return attrs


class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Location
        fields = '__all__'

    def create(self, validated_data):
        location, created = models.Location.objects\
            .get_or_create(**validated_data)
        return location


class EventFeedSerializer(ValidateUserInContextMixin,
                          serializers.ModelSerializer):
    class Meta:
        model = models.Event
        fields = '__all__'

    def create(self, validated_data):
        event = models.Event.objects.create(**validated_data)
        models.Role.objects.create(
            event=event,
            user=self.context.get('request').user,
            name=models.Role.NameChoice.OWNER
        )
        return event


class EventDetailsSerializer(EventFeedSerializer):
    event_contacts = serializers.SerializerMethodField()
    social_media = serializers.SerializerMethodField()
    location = serializers.SerializerMethodField()

    def get_event_contacts(self, event):
        response = []
        for contact in event.event_contact.all():
            response.append({
                'id': contact.id,
                'name': contact.name,
                'phone': str(contact.phone)
            })
        return response

    def get_social_media(self, event):
        response = []
        for media in event.social_media.all():
            response.append({
                'id': media.id,
                'link': media.link,
                'platform': media.platform
            })
        return response

    def get_location(self, event):
        return {
            'id': event.location.id,
            'name': event.location.name,
            'address_line': event.location.address_line,
            'postal_code': event.location.postal_code,
            'country': event.location.country
        }


class RoleSerializer(ValidateUserInContextMixin,
                     serializers.ModelSerializer):
    class Meta:
        model = models.Role
        fields = ['id', 'event', 'user', 'name']
        extra_kwargs = {
            'user': {'read_only': True},
            'name': {'required': False},
        }

    def create(self, validated_data):
        event = validated_data.get('event')
        user = self.context.get("request").user

        if models.Role.objects.filter(event=event, user=user).exists():
            raise ValidationError("Object with given data already exists")

        role = models.Role.objects.create(
            event=validated_data.get('event'),
            user=self.context.get('request').user,
            name=models.Role.NameChoice.USER
        )
        return role

    def update(self, instance, validated_data):
        event = validated_data.get('event')
        user = self.context.get("request").user
        obj = models.Role.objects.filter(event=event, user=user).first()

        if obj and obj != instance:
            raise ValidationError("Object with given data already exists")

        return super().update(instance, validated_data)


class EventContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.EventContact
        fields = '__all__'


class SocialMediaSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.SocialMedia
        fields = '__all__'

    def create(self, validated_data):
        event = validated_data.get('event')
        link = validated_data.get('link')

        if models.SocialMedia.objects.filter(event=event, link=link).exists():
            raise ValidationError("Object with given data already exists")

        return super().create(validated_data)

    def update(self, instance, validated_data):
        event = validated_data.get('event')
        link = validated_data.get('link')
        obj = models.SocialMedia.objects.filter(event=event, link=link).first()

        if obj and obj != instance:
            raise ValidationError("Object with given data already exists")

        return super().update(instance, validated_data)
