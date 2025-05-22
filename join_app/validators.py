import re
from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _
from rest_framework import serializers

class CustomPasswordValidator:
    def validate(self, password, user=None):

        errors = []

        print(f"Raw password: [{password}]")  # Brackets help visualize spaces

        print("CustomPasswordValidator called with:", password)
        if len(password) < 10:
            errors.append(_("Your password must contain at least 10 characters."))
        if not re.search(r'[A-Z]', password):
            errors.append(_("At least one uppercase letter is required."))
        if not re.search(r'[a-z]', password):
            errors.append(_("At least one lowercase letter is required."))
        if not re.search(r'[0-9]', password):
            errors.append(_("At least one digit is required."))
        if not re.search(r'[@$!%+\-/*?&]', password):
            errors.append(_("At least one special character is required (@ $ ! % + - / * ? &)."))
        if re.search(r'\s', password):
            errors.append(_("Password must not contain any spaces."))        
        if errors:
            raise ValidationError(errors)
        
    def get_help_text(self):
        return _(
            "Dein Passwort:\n"
            "- min. 1 Großbuchstabe (A-Z)\n"
            "- min. 1 Kleinbuchstabe (a-z)\n"
            "- min. 1 Zahl (0-9)\n"
            "- min. 1 Sonderzeichen (@ $ ! % + - / * ? &)"
        )

class CustomPhoneValidator:
    def __call__(self, value):
        # Define a regular expression pattern. This example expects an optional plus, followed by 7 to 15 digits.
        pattern = re.compile(r'^(?:\+|00)\d{7,15}$')
        if not pattern.match(value):
            raise serializers.ValidationError(
                "Phone number must be entered in the format: '+4917612121212'. Up to 15 digits allowed."
            )
        return value