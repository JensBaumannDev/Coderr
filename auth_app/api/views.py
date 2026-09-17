from rest_framework import status, generics, permissions
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.views import APIView

from auth_app.models import User

from .permissions import IsOwnerOrReadOnly
from .serializers import (
    RegistrationSerializer,
    LoginSerializer,
    ProfileSerializer,
    ProfileListSerializer,
    CustomerProfileListSerializer,
)


class RegistrationView(APIView):
    """Creates new user accounts and authentication tokens."""

    def post(self, request):
        """Processes a user registration request."""
        serializer = RegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            token = Token.objects.create(user=user)
            data = {
                "token": token.key,
                "username": user.username,
                "email": user.email,
                "user_id": user.id,
            }
            return Response(data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    """Authenticates users and returns authentication tokens."""

    def post(self, request):
        """Processes a user login request."""
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data["user"]
            token, created = Token.objects.get_or_create(user=user)
            data = {
                "token": token.key,
                "username": user.username,
                "email": user.email,
                "user_id": user.id,
            }
            return Response(data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProfileView(generics.RetrieveUpdateAPIView):
    """Retrieves and updates a single user profile."""
    queryset = User.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]


class CustomerProfileListView(generics.ListAPIView):
    """Lists all customer profiles."""
    queryset = User.objects.filter(type="customer")
    serializer_class = CustomerProfileListSerializer
    permission_classes = [permissions.IsAuthenticated]


class BusinessProfileListView(generics.ListAPIView):
    """Lists all business profiles."""
    queryset = User.objects.filter(type="business")
    serializer_class = ProfileListSerializer
    permission_classes = [permissions.IsAuthenticated]
