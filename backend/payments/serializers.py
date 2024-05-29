import decimal

from rest_framework import serializers

from events.mixins import ValidateUserInContextMixin
from payments.models import Order, OrderItem


class OrderItemSerializer(serializers.ModelSerializer):
    total_amount = serializers.SerializerMethodField()

    class Meta:
        model = OrderItem
        fields = '__all__'
        # TODO find better way to pass tests, this is not safe
        extra_kwargs = {'order': {'required': False}}

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep['ticket'] = {
            'id': instance.ticket.id,
            'title': instance.ticket.title,
            'desc': instance.ticket.desc,
            'quantity': instance.ticket.quantity,
            'amount': instance.ticket.amount,
            'event': instance.ticket.event.id
        }
        return rep

    def get_total_amount(self, item):
        return (decimal.Decimal(item.ticket.amount)
                * decimal.Decimal(item.quantity)
                * decimal.Decimal(item.ticket_type))


class OrderSerializer(ValidateUserInContextMixin,
                      serializers.ModelSerializer):
    order_items = OrderItemSerializer(many=True)
    total = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = "__all__"
        extra_kwargs = {'user': {'read_only': True}}

    def get_total(self, order):
        total = 0
        for item in order.order_items.all():
            total += (decimal.Decimal(item.ticket.amount)
                      * decimal.Decimal(item.quantity)
                      * decimal.Decimal(item.ticket_type))

        return total

    def create(self, validated_data):
        user = self.context.get('request').user
        items = validated_data.pop("order_items")

        order = Order.objects.create(user=user, **validated_data)
        if items:
            [item.update(order=order) for item in items]
            OrderItem.objects.bulk_create(
                [OrderItem(**item) for item in items]
            )

        return order
