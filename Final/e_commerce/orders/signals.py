from django.db.models.signals import post_save
from django.dispatch import receiver
from orders.models import OrderItem


@receiver(post_save, sender=OrderItem)
def update_order_total(sender, instance, **kwargs):
    order = instance.order
    order.total_amount = order.calculate_total_amount()
    order.save()
