from celery import shared_task
from django.conf import settings
from django.core.mail import send_mail

from .models import Order


@shared_task(bind=True, max_retries=3)
def send_email_task(order_id):
    try:
        order = Order.objects.get(id=order_id)
        subject = f"Order Confirmation #{order.id}"
        message = f"Thank you for your order, {order.user.first_name}!"
        recipient = [order.user.email]

        send_mail(
            subject=subject,
            message=message,
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[recipient],
        )
        return f"Email has been successfully send to {order.user.email}"
    except Order.DoesNotExist:
        return f"Order with ID {order_id} does not exist."


@shared_task
def process_payment(order_id):
    try:
        order = Order.objects.get(id=order_id)
        if order.status == "pending":
            order.status = "completed"
            order.save()
            return f"Payment processed for Order #{order.id}"
        else:
            return f"Order #{order.id} is already processed."
    except Order.DoesNotExist:
        return f"Order with ID {order_id} does not exist."
