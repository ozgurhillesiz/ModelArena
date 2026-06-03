"""
ModelArena - DRF Serializer'lar
=================================
Django REST Framework serializer'ları — model verilerini
JSON formatına dönüştürür. API endpoint'lerinde kullanılır.
"""

from rest_framework import serializers
from .models import AIModel, Benchmark, PriceHistory, UserFavorite


# Benchmark sonuçları serializer'ı
class BenchmarkSerializer(serializers.ModelSerializer):
    """Model benchmark test sonuçlarını JSON'a dönüştürür."""
    class Meta:
        model = Benchmark
        fields = '__all__'


# Fiyat geçmişi serializer'ı
class PriceHistorySerializer(serializers.ModelSerializer):
    """Model fiyat geçmişi kayıtlarını JSON'a dönüştürür."""
    class Meta:
        model = PriceHistory
        fields = '__all__'


# Ana AI model serializer'ı — benchmark ve fiyat geçmişi iç içe (nested)
class AIModelSerializer(serializers.ModelSerializer):
    """
    AI model verilerini JSON'a dönüştürür.
    Benchmark ve fiyat geçmişi bilgileri nested olarak dahil edilir.
    """
    benchmarks = BenchmarkSerializer(many=True, read_only=True)
    price_history = PriceHistorySerializer(many=True, read_only=True)

    class Meta:
        model = AIModel
        fields = '__all__'


# Favori serializer'ı
class UserFavoriteSerializer(serializers.ModelSerializer):
    """Kullanıcı favori modellerini JSON'a dönüştürür."""
    class Meta:
        model = UserFavorite
        fields = '__all__'