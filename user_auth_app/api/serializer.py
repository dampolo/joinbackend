from rest_framework import serializers
from user_auth_app.models import UserProfile
from django.contrib.auth.models import User

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = '__all__'

class RegistrationSerializer(serializers.ModelSerializer):
    repeated_password = serializers.CharField(write_only=True)

    class Meta:
        Model = User
        fields = ["username", "email", "password", "repeated_password"]
        extra_kwargs = {
            "password": {
                "write_only": True #Only write, you will not see it.
            }
        }