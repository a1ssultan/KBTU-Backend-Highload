from django.db import models

# Create your models here.


class Email(models.Model):
    recipient = models.EmailField()
    subject = models.CharField(max_length=200)
    body = models.TextField()
    sent_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"Email to {self.recipient}: {self.subject}"
