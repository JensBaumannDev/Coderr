from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """Represents a user with a customer or business role."""
    TYPE_CHOICES = [
        ("customer", "Customer"),
        ("business", "Business"),
    ]
    type = models.CharField(max_length=30, choices=TYPE_CHOICES)
    location = models.CharField(max_length=30, blank=True)
    tel = models.CharField(max_length=15, blank=True)
    description = models.TextField(blank=True)
    working_hours = models.CharField(max_length=50, blank=True)
    file = models.ImageField(
        upload_to="profile_pictures/", blank=True, null=True
    )
