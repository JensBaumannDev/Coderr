"""Filtering and sorting helpers for offer querysets."""

from django.db.models import Min, Q
from rest_framework.exceptions import ValidationError


def filter_offers(queryset, parameters):
    """Returns offers with supported filters and sorting applied."""
    queryset = _add_offer_minimums(queryset)
    queryset = _filter_offers(queryset, parameters)
    return _order_offers(queryset, parameters.get("ordering"))


def _add_offer_minimums(queryset):
    """Adds minimum price and delivery time to each offer."""
    return queryset.annotate(
        lowest_price=Min("details__price"),
        shortest_delivery_time=Min("details__delivery_time_in_days"),
    )


def _filter_offers(queryset, parameters):
    """Applies all supported offer filters."""
    queryset = _filter_creator(queryset, parameters.get("creator_id"))
    queryset = _filter_price(queryset, parameters.get("min_price"))
    queryset = _filter_delivery_time(
        queryset, parameters.get("max_delivery_time")
    )
    return _filter_search(queryset, parameters.get("search"))


def _filter_creator(queryset, creator_id):
    """Filters offers by their creator."""
    if creator_id:
        return queryset.filter(user_id=creator_id)
    return queryset


def _filter_price(queryset, min_price):
    """Filters offers by their minimum price."""
    if min_price:
        return queryset.filter(lowest_price__gte=min_price)
    return queryset


def _filter_delivery_time(queryset, max_delivery_time):
    """Filters offers by their shortest delivery time."""
    if max_delivery_time:
        delivery_time = _get_delivery_time(max_delivery_time)
        return queryset.filter(shortest_delivery_time__lte=delivery_time)
    return queryset


def _get_delivery_time(value):
    """Returns a delivery time or raises a validation error."""
    try:
        return int(value)
    except ValueError as error:
        raise ValidationError(
            {"max_delivery_time": "Must be an integer."}
        ) from error


def _filter_search(queryset, search):
    """Searches offer titles and descriptions."""
    if search:
        return queryset.filter(
            Q(title__icontains=search) | Q(description__icontains=search)
        )
    return queryset


def _order_offers(queryset, ordering):
    """Orders offers by a supported field."""
    if ordering == "min_price":
        return queryset.order_by("lowest_price")
    if ordering == "updated_at":
        return queryset.order_by(ordering)
    return queryset.order_by("-created_at")
