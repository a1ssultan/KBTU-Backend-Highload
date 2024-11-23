from django.db import models

# Create your models here.


class UserProfile(models.Model):
    name = models.CharField(max_length=100)
    age = models.IntegerField()
    website = models.URLField()
    email = models.EmailField()

    def __str__(self):
        return self.name
