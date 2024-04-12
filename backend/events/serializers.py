from django.utils.translation import gettext_lazy as _

from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from events import models


class ValidateUserInContextMixin:
    def validate(self, attrs):
        request = self.context.get("request")

        if not hasattr(request, "user") and request.method != 'GET':
            raise ValidationError(_("Serializer is missing user in context"))

        return attrs


class LocationSerializer(serializers.Serializer):
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


class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Role
        fields = '__all__'


class EventContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.EventContact
        fields = '__all__'


class SocialMediaSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.SocialMedia
        fields = '__all__'
