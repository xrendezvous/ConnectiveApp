from django.core.validators import RegexValidator
from django.forms import ModelForm, CharField, TextInput, DateInput, BooleanField, CheckboxInput, DateField, EmailField

from .models import Contact, Address


class ContactForm(ModelForm):
    name = CharField(min_length=3, max_length=20, required=True,
                     widget=TextInput(attrs={'placeholder': "*Ім'я"}))
    surname = CharField(min_length=3, max_length=20, required=False,
                        widget=TextInput(attrs={'placeholder': 'Прізвище'}))
    email = EmailField(required=False,
                      widget=TextInput(attrs={'placeholder': 'Email'}))
    mobile_phone = CharField(required=False, validators=[RegexValidator(
        regex=r'\+?\d{1,3}\(?\d{2,4}\)?\d{3}(?:-?\d{3,4})(\d{3})?',
        message='Номер телефону необхідно вводити у форматі: '
                '+Код країни (код оператора)номер телефону Приклад: +380(50)1234567. Допускається до 15 цифр.'
    )],
                             widget=TextInput(attrs={'placeholder': 'Номер телефону', "class": "form-control"}))
    work_phone = CharField(required=False, validators=[RegexValidator(
        regex=r'\+?\d{1,3}\(?\d{2,4}\)?\d{3}(?:-?\d{3,4})(\d{3})?',
        message='Номер телефону необхідно вводити у форматі: '
                '+Код країни (код оператора)номер телефону Приклад: +380(50)1234567. Допускається до 15 цифр.'
    )],
                           widget=TextInput(attrs={'placeholder': 'Робочий телефон', "class": "form-control"}))
    home_phone = CharField(required=False, validators=[RegexValidator(
        regex=r'\+?\d{1,3}\(?\d{2,4}\)?\d{3}(?:-?\d{3,4})(\d{3})?',
        message='Номер телефону необхідно вводити у форматі: '
                '+Код країни (код оператора)номер телефону Приклад: +380(50)1234567. Допускається до 15 цифр.'
    )],
                           widget=TextInput(attrs={'placeholder': 'Домашній телефон', "class": "form-control"}))
    birthdate = DateField(required=False, input_formats=['%d/%m/%Y'], widget=DateInput(format='%d/%m/%Y'))
    facebook = CharField(required=False, validators=[RegexValidator(
        regex=r'^https?://(www\.)?facebook\.com/.+',
        message='Enter a valid Facebook URL.',
    )], widget=TextInput(attrs={'placeholder': 'https://facebook.com', "class": "form-control"}))
    instagram = CharField(required=False, validators=[RegexValidator(
        regex=r'^https?://(www\.)?instagram\.com/.+',
        message='Enter a valid Instagram URL.',
    )], widget=TextInput(attrs={"placeholder": 'https://instagram.com', "class": "form-control"}))
    tiktok = CharField(required=False, validators=[RegexValidator(
        regex=r'^https?://(www\.)?tiktok\.com/.+',
        message='Enter a valid Tiktok URL.',
    )], widget=TextInput(attrs={"placeholder": 'https://tiktok.com', "class": "form-control"}))
    is_favorite = BooleanField(required=False, label='Is favorite',
                               widget=CheckboxInput(attrs={'placeholder': 'is_favorite', "class": "form-check-input"}))

    class Meta:
        model = Contact
        fields = ['name', 'surname', 'email', 'mobile_phone', 'work_phone', 'home_phone', 'birthdate', 'is_favorite',
                  'facebook', 'instagram', 'tiktok', ]
        widgets = {
            'birthdate': DateInput(attrs={'type': 'date'}),
        }


class AddressForm(ModelForm):
    country = CharField(required=False, widget=TextInput(attrs={'placeholder': 'Країна', "class": "form-control"}))
    city = CharField(required=False, widget=TextInput(attrs={'placeholder': 'Місто', "class": "form-control"}))
    address = CharField(required=False, widget=TextInput(attrs={'placeholder': 'Адреса', "class": "form-control"}))

    class Meta:
        model = Address
        fields = ['country', 'city', 'address']