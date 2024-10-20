from django.db import models

from django.contrib.auth.models import AbstractUser
from phonenumber_field.modelfields import PhoneNumberField


class User(AbstractUser):
    phone_number = PhoneNumberField(blank=False, null=False, unique=True, db_index=True)
    address = models.TextField(blank=False, null=False)

    def save(self, *args, **kwargs):
        if self.pk is None or not self.password.startswith("pbkdf2_sha256$"):
            self.set_password(self.password)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.username
