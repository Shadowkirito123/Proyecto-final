from django.core.validators import RegexValidator

class NoSpecialCharactersValidator(RegexValidator):
    regex = r'^[a-zA-Z0-9]+$'
    message = 'No se permiten caracteres especiales'