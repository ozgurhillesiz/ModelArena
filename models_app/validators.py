"""
ModelArena - Özel Şifre Validator'ı
======================================
Django'nun varsayılan şifre kurallarını genişletir.
Büyük harf, rakam ve özel karakter zorunluluğu ekler.
settings.py'de AUTH_PASSWORD_VALIDATORS listesine tanımlanır.
"""

import re
from django.core.exceptions import ValidationError


class CustomPasswordValidator:
    """
    Güçlü şifre kurallarını zorunlu kılan validator.
    En az 1 büyük harf, 1 rakam ve 1 özel karakter gerektirir.
    """

    def validate(self, password, user=None):
        """Şifreyi kurallara göre doğrular, geçersizse ValidationError fırlatır."""
        if not re.search(r'[A-Z]', password):
            raise ValidationError('Şifre en az 1 büyük harf içermelidir.')
        if not re.search(r'[0-9]', password):
            raise ValidationError('Şifre en az 1 rakam içermelidir.')
        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
            raise ValidationError('Şifre en az 1 özel karakter içermelidir (!@#$% gibi).')

    def get_help_text(self):
        """Kullanıcıya gösterilecek şifre kural açıklamasını döndürür."""
        return 'Şifreniz en az 1 büyük harf, 1 rakam ve 1 özel karakter içermelidir.'