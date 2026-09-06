from django.urls import path
from .views import (
    RegistrationView,
    LoginView,
    ProfileView,
    BusinessProfileListView,
    CustomerProfileListView,
)

urlpatterns = [
    path("registration/", RegistrationView.as_view(), name="registration"),
    path("login/", LoginView.as_view(), name="login"),
    path("profile/<int:pk>/", ProfileView.as_view(), name="profile"),
    path(
        "profiles/business/",
        BusinessProfileListView.as_view(),
        name="profiles-business",
    ),
    path(
        "profiles/customer/",
        CustomerProfileListView.as_view(),
        name="profiles-customer",
    ),
]
