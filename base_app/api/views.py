from django.db.models import Avg
from rest_framework.response import Response
from rest_framework.views import APIView

from auth_app.models import User
from offers_app.models import Offer
from reviews_app.models import Review


class BaseInfoView(APIView):
    """Provides general platform statistics."""

    def get(self, request):
        """Returns the current platform statistics."""
        return Response(
            {
                "review_count": Review.objects.count(),
                "average_rating": self._average_rating(),
                "business_profile_count": self._business_profile_count(),
                "offer_count": Offer.objects.count(),
            }
        )

    def _average_rating(self):
        """Calculates the average review rating."""
        average_rating = Review.objects.aggregate(
            average=Avg("rating")
        )["average"]
        return round(average_rating or 0, 1)

    def _business_profile_count(self):
        """Counts all business user profiles."""
        return User.objects.filter(type="business").count()
