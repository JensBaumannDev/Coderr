"""Filtering and sorting helpers for review querysets."""


def filter_reviews(queryset, parameters):
    """Returns reviews with supported filters and sorting applied."""
    queryset = _filter_business_user(
        queryset, parameters.get("business_user_id")
    )
    queryset = _filter_reviewer(queryset, parameters.get("reviewer_id"))
    return _order_reviews(queryset, parameters.get("ordering"))


def _filter_business_user(queryset, business_user_id):
    """Filters reviews by business user."""
    if business_user_id:
        return queryset.filter(business_user_id=business_user_id)
    return queryset


def _filter_reviewer(queryset, reviewer_id):
    """Filters reviews by reviewer."""
    if reviewer_id:
        return queryset.filter(reviewer_id=reviewer_id)
    return queryset


def _order_reviews(queryset, ordering):
    """Orders reviews by a supported field."""
    allowed_orderings = ["updated_at", "-updated_at", "rating", "-rating"]
    if ordering in allowed_orderings:
        return queryset.order_by(ordering)
    return queryset.order_by("-updated_at")
