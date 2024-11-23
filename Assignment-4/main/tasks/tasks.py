from celery import shared_task
from django.core.mail import send_mail
from .models import Email
from django.conf import settings


@shared_task(bind=True, max_retries=3)
def send_email_task(self, email_id: int):
    try:
        email = Email.objects.get(id=email_id)
        send_mail(
            subject=email.subject,
            message=email.body,
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[email.recipient],
        )
        return f"Email has been successfully sent to {email.recipient}"
    except Exception as exc:
        self.retry(exc=exc, countdown=60)
