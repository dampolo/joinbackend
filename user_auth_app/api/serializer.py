from rest_framework import serializers
from user_auth_app.models import UserProfile
from django.contrib.auth.models import User
from join_app.models import Contact
from phonenumber_field.modelfields import PhoneNumberField
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError as DjangoValidationError
from join_app.validators import CustomPhoneValidator


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = "__all__"

class LoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["username", "email"]
        extra_kwargs = {
            "username": {
                "required": False
            }
        }

class RegistrationSerializer(serializers.ModelSerializer):
    repeated_password = serializers.CharField(write_only=True)
    phone = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ["username", "first_name", "last_name", "email", "password", "repeated_password", "phone"]
        extra_kwargs = {
            "password": {
                "write_only": True  # Only write, you will not see it.
            },
        }
    
    def validate_phone(self, value):
        validator = CustomPhoneValidator()
        return validator.__call__(value)
    
    
    def save(self):
        phone = self.validated_data.pop("phone")
        pw = self.validated_data["password"]
        repeated_pw = self.validated_data["repeated_password"]


        if pw != repeated_pw:
            raise serializers.ValidationError(
                {"password": "Passwords don't match"})
        
        try:
            validate_password(password=pw)
        except DjangoValidationError as error:
            raise serializers.ValidationError({"password": error.messages})

        if User.objects.filter(email=self.validated_data["email"]).exists():
            raise serializers.ValidationError("This email exists already")
        
        if Contact.objects.filter(phone=phone).exists():
            raise serializers.ValidationError("This phone exists already")

        account = User(
            username=self.validated_data["username"],
            email=self.validated_data["email"],
            first_name=self.validated_data["first_name"],
            last_name=self.validated_data["last_name"],
        )
        account.set_password(pw)
        account.save()

        user_profile = UserProfile.objects.create(user=account, phone=phone)

        Contact.objects.create(
            name=account.first_name + " " +  account.last_name,
            email=account.email,
            phone=user_profile.phone
        )
        return account
