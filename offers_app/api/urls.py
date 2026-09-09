from django.urls import path
from .views import OfferListView, OfferDetailRetrieveView, OfferDetailView

urlpatterns = [
    path("offers/", OfferListView.as_view(), name="offers"),
    path("offerdetails/<int:pk>/", OfferDetailRetrieveView.as_view(),name="offerdetail"),
    path("offers/<int:pk>/", OfferDetailView.as_view(), name="offer-detail"),
]
