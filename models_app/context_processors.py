from django.contrib.auth.models import User
from .models import AIModel, Review, UserFavorite


def admin_stats(request):
    # Sadece admin sayfalarında çalışsın
    if not request.path.startswith('/gizli-admin-ma2026/'):
        return {}
    return {
        'ma_total_models': AIModel.objects.count(),
        'ma_total_users': User.objects.count(),
        'ma_total_reviews': Review.objects.count(),
        'ma_total_favorites': UserFavorite.objects.count(),
    }