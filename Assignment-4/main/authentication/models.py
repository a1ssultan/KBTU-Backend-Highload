from django.db import models
from encrypted_model_fields.fields import EncryptedCharField, EncryptedEmailField


class UserProfile(models.Model):
    name = models.CharField(max_length=100)
    age = models.IntegerField()
    website = models.URLField()
    email = EncryptedEmailField()
    phone_number = EncryptedCharField(max_length=15, null=True)
    address = EncryptedCharField(max_length=255, null=True)

    class Meta:
        indexes = [
            models.Index(fields=['name']),
            models.Index(fields=['email']),
            models.Index(fields=['phone_number']),
        ]

    def __str__(self):
        return self.name
