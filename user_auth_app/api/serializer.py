from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from user_auth_app.models import UserProfile
from django.contrib.auth.models import User
from join_app.models import Contact
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError as DjangoValidationError
from django.core.validators import MinLengthValidator
from join_app.validators import CustomPhoneValidator, CustomPasswordValidator
from django.contrib.auth import authenticate


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = "__all__"

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        username = data.get("username", "").lower()
        password = data.get("password")

        user = authenticate(username=username, password=password)

        if user is None:
            raise serializers.ValidationError({
                "message": "Oops! Wrong password or username. Please try again."  # <-- your custom message
            })

        data["user"] = user
        return data

class RegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, trim_whitespace=False)
    repeated_password = serializers.CharField(write_only=True, trim_whitespace=False)
    phone = serializers.CharField(write_only=True)
    username = serializers.CharField()
    first_name = serializers.CharField(validators=[MinLengthValidator(3)])
    last_name = serializers.CharField(validators=[MinLengthValidator(3)])
    email = serializers.EmailField()
    help_text = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ["username", "first_name", "last_name", "email", "password", "repeated_password", "phone", "help_text"]
        extra_kwargs = {
            "password": {
                "write_only": True  # Only write, you will not see it.
            },
        }

    def get_help_text(self, obj):
        return CustomPasswordValidator().get_help_text()

    def validate_username(self, value):
        value = value.lower()
        try:
            MinLengthValidator(3)(value)
        except DjangoValidationError as error:
            raise serializers.ValidationError(error.messages)
            # Check uniqueness
        if User.objects.filter(username__iexact=value).exists():
            raise serializers.ValidationError("This username exists already.")
        return value
    
    def validate_password(self, value):
        repeated_pw = self.initial_data.get("repeated_password")        
        # Custom complexity validation
        try:
            CustomPasswordValidator().validate(value)
        except DjangoValidationError as error:
            raise serializers.ValidationError(error.messages)
        
        if repeated_pw and value != repeated_pw:
            raise serializers.ValidationError("Passwords don't match.")
        return value
    
    def validate_email(self, value):
        value = value.lower()
        if User.objects.filter(email__iexact=value).exists():
            raise serializers.ValidationError("This email exists already.")
        return value
    
    def validate_phone(self, value):
        validator = CustomPhoneValidator()
        validator(value)

        if Contact.objects.filter(phone=value).exists():
            raise serializers.ValidationError("This phone exists already.")
        return value
    
    def save(self):
        pw = self.validated_data["password"]
        phone = self.validated_data["phone"]

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
            name=f"{account.first_name} {account.last_name}",
            email=account.email,
            phone=user_profile.phone
        )
        return account