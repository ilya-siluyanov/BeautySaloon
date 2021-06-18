from django.core.exceptions import ValidationError


def validate_phone_number(value: str):
    validation_error = ValidationError('Введите корректный номер телефона: +7ХХХХХХХХХХ')
    if type(value) is not str:
        raise validation_error
    if not value.startswith('+'):
        raise validation_error
    if len(value) != 12:
        raise validation_error
    try:
        int(value[1:])
    except ValueError:
        raise validation_error
