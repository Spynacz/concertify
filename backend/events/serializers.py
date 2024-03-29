from rest_framework import serializers

from events import models


class EventSerializer(serializers.ModelSerializer):
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
