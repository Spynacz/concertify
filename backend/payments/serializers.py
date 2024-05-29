import decimal

from rest_framework import serializers

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
        # When in cart, instance is an OrderedDict
        try:
            ticket = instance['ticket']
        # When saved in checkout, instance is a model
        except (TypeError):
            ticket = instance.ticket

        rep['ticket'] = {
            'id': ticket.id,
            'title': ticket.title,
            'desc': ticket.desc,
            'quantity': ticket.quantity,
            'amount': ticket.amount,
            'event': ticket.event.id
        }
        return rep

    def get_total_amount(self, item):
        # When in cart, item is an OrderedDict
        try:
            return (decimal.Decimal(item['ticket'].amount)
                    * decimal.Decimal(item['quantity'])
                    * decimal.Decimal(item['ticket_type']))
        # When saved in checkout, item is a model
        except (TypeError):
            return (decimal.Decimal(item.ticket.amount)
                    * decimal.Decimal(item.quantity)
                    * decimal.Decimal(item.ticket_type))


class OrderSerializer(serializers.ModelSerializer):
    order_items = OrderItemSerializer(many=True)
    total = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = "__all__"
        extra_kwargs = {'user': {'read_only': True}}

    def get_total(self, order):
        total = 0
        # When in cart, order is an OrderedDict
        try:
            for item in order['order_items']:
                total += (decimal.Decimal(item['ticket'].amount)
                          * decimal.Decimal(item['quantity'])
                          * decimal.Decimal(item['ticket_type']))
        # When saved in checkout, order is a model
        except (TypeError):
            for item in order.order_items.all():
                total += (decimal.Decimal(item.ticket.amount)
                          * decimal.Decimal(item.quantity)
                          * decimal.Decimal(item.ticket_type))

        return total

    def create(self, validated_data):
        items = validated_data.pop("order_items")

        order = Order.objects.create(**validated_data)
        if items:
            [item.update(order=order) for item in items]
            OrderItem.objects.bulk_create(
                [OrderItem(**item) for item in items]
            )

        return order
