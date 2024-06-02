from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    LANGUAGE_CHOICES = (
        ('English', 'English'),
        ('Chinese', 'Chinese'),
        ('Japanese', 'Japanese'),
        ('Korean', 'Korean'),
    )
    language = models.CharField(max_length=10, choices=LANGUAGE_CHOICES)
