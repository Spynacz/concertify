from rest_framework import serializers

from events import models


class EventSerializer(serializers.ModelSerializer):
    class Meta:
        models = models.Event
        fields = '__all__'


class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Role
        fields = '__all__'
