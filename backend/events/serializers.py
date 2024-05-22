import decimal

from django.utils import timezone

from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from events import models
from events.mixins import CreateNotificationMixin, ValidateUserInContextMixin
from users import models as users_models


class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Location
        fields = '__all__'

    def create(self, validated_data):
        location, created = models.Location.objects\
            .get_or_create(**validated_data)
        return location


class EventFeedSerializer(ValidateUserInContextMixin,
                          serializers.ModelSerializer,
                          CreateNotificationMixin):
    class Meta:
        model = models.Event
        fields = '__all__'

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep['location'] = self.get_location(instance)
        return rep

    def create(self, validated_data):
        event = models.Event.objects.create(**validated_data)
        models.Role.objects.create(
            event=event,
            user=self.context.get('request').user,
            name=models.Role.NameChoice.OWNER
        )
        self._schedule_reminder(event)
        return event

    def update(self, instance, validated_data):
        self.revoke_task(instance)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        self._schedule_reminder(instance)
        return instance

    def get_location(self, event):
        return {
            'id': event.location.id,
            'address_line': event.location.address_line,
        }


class EventDetailsSerializer(EventFeedSerializer):
    event_contacts = serializers.SerializerMethodField()
    social_media = serializers.SerializerMethodField()
    ticket = serializers.SerializerMethodField()

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

    def get_ticket(self, event):
        response = []
        for ticket in event.ticket.all():
            response.append({
                'id': ticket.id,
                'title': ticket.title,
                'desc': ticket.desc,
                'quantity': ticket.quantity,
                'amount': ticket.amount
            })
        return response


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


class ScheduleItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ScheduleItem
        fields = "__all__"

    def validate_when(self, when):
        if when < timezone.now():
            msg = "You can't create a schedule with items in the past"
            raise ValidationError(msg)

        return when


class TicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Ticket
        fields = "__all__"

    def validate_quantity(self, quantity):
        if quantity < 0:
            raise ValidationError("Ticket quantity cannot be lower than 0")

        return quantity

    def validate_amount(self, amount):
        if amount < 0:
            raise ValidationError("Amount cannot be lower than 0")

        return amount


class CartItemSerializer(serializers.Serializer):
    TICKET_CHOICES = [
        (.5, 'REDUCED'),
        (1, 'REGULAR')
    ]
    ticket_type = serializers.ChoiceField(choices=TICKET_CHOICES)
    quantity = serializers.IntegerField()
    amount = serializers.DecimalField(max_digits=9, decimal_places=2)
    ticket = serializers.IntegerField()
    total_amount = serializers.SerializerMethodField()

    class Meta:
        fields = "__all__"

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        id = instance.get('ticket')
        ticket = models.Ticket.objects.get(id=id)
        rep['ticket'] = {
            'id': ticket.id,
            'title': ticket.title,
            'desc': ticket.desc,
            'quantity': ticket.quantity,
            'amount': ticket.amount,
            'event': ticket.event.id
        }
        return rep

    def get_total_amount(self, cart_item):
        return (decimal.Decimal(cart_item.get("amount"))
                * decimal.Decimal(cart_item.get("quantity"))
                * decimal.Decimal(cart_item.get("ticket_type")))


class CartSerializer(serializers.Serializer):
    items = CartItemSerializer(many=True)
    total = serializers.SerializerMethodField()

    class Meta:
        fields = "__all__"

    def get_total(self, cart):
        total = 0
        for item in cart.get("items"):
            total += (decimal.Decimal(item.get("amount"))
                      * decimal.Decimal(item.get("quantity"))
                      * decimal.Decimal(item.get("ticket_type")))

        return total


class NotificationSerializer(serializers.ModelSerializer,
                             CreateNotificationMixin):
    class Meta:
        model = users_models.Notification
        fields = ['title', 'desc', 'notification_type']

    def create(self, validated_data):
        request = self.context.get('request')
        pk = request.parser_context['kwargs'].get('pk')
        users = users_models.ConcertifyUser.objects.filter(
            role__event_id=pk,
            role__name=models.Role.NameChoice.USER
        )
        template = users_models.Notification(**validated_data)
        self.create_notifications_for_users(template, users)
        return template
