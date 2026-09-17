from django.contrib.auth import get_user_model

from reviews_app.models import Review


class ReviewTestMixin:
    def create_user(self, username, user_type="customer"):
        return get_user_model().objects.create_user(
            username=username,
            password="testpass123",
            type=user_type,
        )

    def create_review(
        self,
        business_user,
        reviewer,
        rating=5,
        description="Sehr gute Arbeit",
    ):
        return Review.objects.create(
            business_user=business_user,
            reviewer=reviewer,
            rating=rating,
            description=description,
        )
