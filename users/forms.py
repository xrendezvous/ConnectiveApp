from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.forms import CharField, TextInput, EmailField, EmailInput, PasswordInput
from users.validators import validate_email, validate_username


class RegisterForm(UserCreationForm):
    username = CharField(
        max_length=50,
        min_length=3,
        required=True,
        validators=[validate_username],
        widget=TextInput(attrs={"class": "form-control"}),
        error_messages={
            'required': "Це поле обов'язкове.",
            'max_length': "Ім'я користувача повинно містити не більше 50 символів.",
            'min_length': "Ім'я користувача повинно містити щонайменше 3 символи.",
            'unique': "Користувач з таким ім'ям вже існує."
        }
    )
    email = EmailField(
        max_length=320,
        validators=[validate_email],
        required=True,
        widget=EmailInput(attrs={"class": "form-control"}),
        error_messages={
            'required': "Це поле обов'язкове.",
            'max_length': "Email повинен містити не більше 320 символів.",
            'invalid': "Введіть правильну email адресу.",
        }
    )
    password1 = CharField(
        required=True,
        widget=PasswordInput(attrs={"class": "form-control"}),
        error_messages={
            'required': "Це поле обов'язкове.",
        }
    )
    password2 = CharField(
        required=True,
        widget=PasswordInput(attrs={"class": "form-control"}),
        error_messages={
            'required': "Це поле обов'язкове.",
        }
    )

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")


class LoginForm(AuthenticationForm):
    username = CharField(
        max_length=50,
        min_length=3,
        required=True,
        widget=TextInput(attrs={"class": "form-control"}),
        error_messages={
            'required': "Це поле обов'язкове.",
            'max_length': "Ім'я користувача повинно містити не більше 50 символів.",
            'min_length': "Ім'я користувача повинно містити щонайменше 3 символи.",
        }
    )
    password = CharField(
        required=True,
        widget=PasswordInput(attrs={"class": "form-control"}),
        error_messages={
            'required': "Це поле обов'язкове.",
        }
    )

    error_messages = {
        'invalid_login':
            "Будь ласка, введіть коректне ім'я користувача і пароль. Зверніть увагу, що обидва поля можуть бути чутливими до регістру.",
    }

    class Meta:
        model = User
        fields = ("username", "password")
