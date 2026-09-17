from django.db import models
from auth_app.models import User
from offers_app.models import OfferDetail


class Order(models.Model):
    """Represents an order created from an offer package."""
    STATUS_CHOICES = [
        ("in_progress", "In Progress"),
        ("completed", "Completed"),
        ("cancelled", "Cancelled"),
    ]

    customer_user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="customer_orders"
    )
    business_user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="business_orders"
    )
    title = models.CharField(max_length=100)
    revisions = models.IntegerField()
    delivery_time_in_days = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    features = models.JSONField(default=list)
    offer_type = models.CharField(
        max_length=20,
        choices=OfferDetail.TYPE_CHOICES,
    )
    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default="in_progress"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        """Returns the order title."""
        return f"Order #{self.id}: {self.title}"
