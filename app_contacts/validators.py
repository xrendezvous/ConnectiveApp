from django.core.exceptions import ValidationError
import re


def validate_phone_number(value):
    phone_regex = re.compile(r'\+?\d{1,3}\(?\d{2,4}\)?\d{3}(?:-?\d{3,4})(\d{3})?')
    if not phone_regex.fullmatch(value):
        raise ValidationError(
            'Номер телефону необхідно вводити у форматі: +Код країни (код оператора)номер телефону. Допускаються тільки числа. Приклад: +380(50)1234567. Допускається до 20 цифр.'
        )
