"""
ModelArena - Context Processor'lar
=====================================
Admin paneli dashboard'u için istatistik verilerini
template context'ine ekler. Sadece admin sayfalarında çalışır.
settings.py'de TEMPLATES context_processors listesine tanımlanır.
"""

from django.contrib.auth.models import User
from .models import AIModel, Review, UserFavorite


def admin_stats(request):
    """
    Admin dashboard istatistiklerini context'e ekler.
    Performans için sadece admin URL'lerinde veritabanı sorgusu çalıştırır.
    """
    # Sadece admin sayfalarında çalışsın — gereksiz sorguları önler
    if not request.path.startswith('/gizli-admin-ma2026/'):
        return {}
    return {
        'ma_total_models': AIModel.objects.count(),
        'ma_total_users': User.objects.count(),
        'ma_total_reviews': Review.objects.count(),
        'ma_total_favorites': UserFavorite.objects.count(),
    }