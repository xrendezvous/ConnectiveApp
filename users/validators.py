from django.core.exceptions import ValidationError
from django.contrib.auth.models import User


def validate_email(value):
    """
    Validate if the provided email is unique.
    This function checks if the email already exists in the User model.

    Args:
    value (str): The email value to be validated.

    Raises:
    ValidationError: If a user with the provided email already exists.

    Returns:
    None
    """
    if User.objects.filter(email=value).exists():
        raise ValidationError("Користувач з такою поштою вже існує.")


def validate_username(value):
    if User.objects.filter(username=value).exists():
        raise ValidationError("Користувач з таким ім'ям вже існує.")
