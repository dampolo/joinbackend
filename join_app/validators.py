import re
from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _

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