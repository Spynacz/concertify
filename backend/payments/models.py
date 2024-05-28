from django.db import models


class Order(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey('users.ConcertifyUser', related_name='orders',
                             on_delete=models.CASCADE)


class OrderItem(models.Model):
    class TicketTypeChoice(models.TextChoices):
        REDUCED = (.5, 'REDUCED')
        REGULAR = (1, 'REGULAR')

    ticket_type = models.CharField(choices=TicketTypeChoice.choices)
    quantity = models.IntegerField()
    amount = models.DecimalField(max_digits=9, decimal_places=2)
    order = models.ForeignKey(Order, related_name='order_items',
                              on_delete=models.CASCADE)
    ticket = models.ForeignKey('events.Ticket', related_name='order_items',
                               on_delete=models.DO_NOTHING)
