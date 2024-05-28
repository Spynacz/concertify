import decimal

from rest_framework import serializers

from events import models
from payments.models import Order, OrderItem


class CartItemSerializer(serializers.Serializer):
    # TODO add mock saving, and bought ticket history?
    total_amount = serializers.SerializerMethodField()

    class Meta:
        model = OrderItem
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
    total = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = "__all__"

    def get_total(self, cart):
        total = 0
        for item in cart.get("items"):
            total += (decimal.Decimal(item.get("amount"))
                      * decimal.Decimal(item.get("quantity"))
                      * decimal.Decimal(item.get("ticket_type")))

        return total
