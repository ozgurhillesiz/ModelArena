import re
from django.core.exceptions import ValidationError

class CustomPasswordValidator:
    def validate(self, password, user=None):
        if not re.search(r'[A-Z]', password):
            raise ValidationError('Şifre en az 1 büyük harf içermelidir.')
        if not re.search(r'[0-9]', password):
            raise ValidationError('Şifre en az 1 rakam içermelidir.')
        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
            raise ValidationError('Şifre en az 1 özel karakter içermelidir (!@#$% gibi).')

    def get_help_text(self):
        return 'Şifreniz en az 1 büyük harf, 1 rakam ve 1 özel karakter içermelidir.'