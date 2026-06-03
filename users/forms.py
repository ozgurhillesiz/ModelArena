"""
ModelArena - Kullanıcı Formları
=================================
Allauth'un varsayılan kayıt formunu genişleterek
ad ve soyad alanlarını kayıt sürecine ekler.
"""

from allauth.account.forms import SignupForm
from django import forms


class CustomSignupForm(SignupForm):
    """
    Özel kayıt formu — allauth SignupForm'a ad ve soyad alanları ekler.
    settings.py'de ACCOUNT_FORMS ile tanımlanır.
    """
    first_name = forms.CharField(max_length=30, label='Ad', required=True)
    last_name = forms.CharField(max_length=30, label='Soyad', required=True)

    def save(self, request):
        """Kullanıcıyı kaydeder ve first_name/last_name alanlarını doldurur."""
        user = super().save(request)
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.save()
        return user