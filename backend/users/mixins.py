from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError as DjangoValidationError

from rest_framework.exceptions import ValidationError


class ValidatePasswordMixin:
    def validate_password(self, password):
        try:
            validate_password(password)
        except DjangoValidationError as e:
            raise ValidationError(e.messages)
        return password
