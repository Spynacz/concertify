from rest_framework import serializers

from events.models import Event, Role


class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = '__all__'

    def create(self, validated_data):
        event = Event.objects.create(**validated_data)
        Role.objects.create(
            event=event,
            user=self.context.get('request').user,
            name=Role.NameChoice.OWNER
        )
        return event


class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = '__all__'
