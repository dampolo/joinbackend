import re
from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _
from rest_framework import serializers

class CustomPasswordValidator:
    def validate(self, password, user=None):
        if not re.search(r'[A-Z]', password):
            raise ValidationError(_("At least one uppercase letter is required."))
        if not re.search(r'[a-z]', password):
            raise ValidationError(_("At least one lowercase letter is required."))
        if not re.search(r'[0-9]', password):
            raise ValidationError(_("At least one digit is required."))
        if not re.search(r'[@$!%+\-/*?&]', password):
            raise ValidationError(_("At least one special character is required (@ $ ! % + - / * ? &)."))

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
        pattern = re.compile(r'^\+?\d{7,15}$')
        if not pattern.match(value):
            raise serializers.ValidationError(
                "Phone number must be entered in the format: '+4917612121212'. Up to 15 digits allowed."
            )
        print(f'DATA: {self.value}')
        return value