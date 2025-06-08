from rest_framework import generics
from user_auth_app.models import UserProfile
from .serializer import UserProfileSerializer, RegistrationSerializer, LoginSerializer
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework import status
from django.contrib.auth.models import User
from django.utils.crypto import get_random_string
from phonenumber_field.phonenumber import PhoneNumber
from join_app.models import Contact

class UserProfileList(generics.ListCreateAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer

class UserProfileDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer

class CustomLoginView(ObtainAuthToken):
    permission_classes = [AllowAny]
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        data = {}
        if serializer.is_valid():
            user = serializer.validated_data["user"]
            token, created = Token.objects.get_or_create(user=user)
            data = {
                "token": token.key,
                "id": user.id,
                "username": user.username,
                "email": user.email,
                "last_name": user.last_name
            }
            return Response(data, status=status.HTTP_202_ACCEPTED)
        field_names = [
            "username", "password"
        ]
        for field in field_names:
            if field in serializer.errors:
                return Response(serializer.errors, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        return Response(serializer.errors, status=status.HTTP_401_UNAUTHORIZED)


class GuestLoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        # Create a unique username to avoid duplicates
        unique_suffix = get_random_string(2)
        guest_username = f"Guest_{unique_suffix}"
        guest_email = f"{guest_username.lower()}@guest.local"
        guest_password = get_random_string(length=12)


        # Create the guest user
        guest_user = User.objects.create_user(
            username=guest_username,
            email=guest_email,
            password=guest_password,
            first_name="Guest",
            last_name="User"
        )

        # Assign a default phone number (can randomize if needed)
        phone_number = PhoneNumber.from_string("+49123123")  # Adjust format if needed

        # Create profile
        user_profile = UserProfile.objects.create(user=guest_user, phone=phone_number)

        # Add to contacts
        Contact.objects.create(
            name=f"{guest_user.first_name} {guest_user.last_name}",
            email=guest_user.email,
            phone=user_profile.phone
        )

        # Generate token
        token, _ = Token.objects.get_or_create(user=guest_user)

        return Response({
            "token": token.key,
            "id": guest_user.id,
            "username": guest_user.username,
            "email": guest_user.email,
            "is_guest": True,
        }, status=status.HTTP_201_CREATED)

class RegistrationView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = RegistrationSerializer(data=request.data)

        data = {}
        if serializer.is_valid():
            saved_account = serializer.save()
            token, created = Token.objects.get_or_create(user=saved_account)
            data = {
                "token": token.key,
                "username": saved_account.username,
                "email": saved_account.email
            }
            return Response(data, status=status.HTTP_201_CREATED)
        
        field_names = [
            "username", "first_name", "last_name",
            "email", "password", "repeated_password", "phone"
        ]
        for field in field_names:
            if field in serializer.errors:
                return Response(serializer.errors, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)