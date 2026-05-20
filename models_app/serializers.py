from rest_framework import serializers
from .models import AIModel, Benchmark, PriceHistory, UserFavorite

class BenchmarkSerializer(serializers.ModelSerializer):
    class Meta:
        model = Benchmark
        fields = '__all__'

class PriceHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = PriceHistory
        fields = '__all__'

class AIModelSerializer(serializers.ModelSerializer):
    benchmarks = BenchmarkSerializer(many=True, read_only=True)
    price_history = PriceHistorySerializer(many=True, read_only=True)
    
    class Meta:
        model = AIModel
        fields = '__all__'

class UserFavoriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserFavorite
        fields = '__all__'