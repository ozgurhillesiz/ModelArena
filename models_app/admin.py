from django.contrib import admin
from .models import AIModel, Benchmark, PriceHistory, UserFavorite, Review, SubscriptionPlan, UserProfile, Notification

@admin.register(AIModel)
class AIModelAdmin(admin.ModelAdmin):
    list_display = ['name', 'company', 'input_price', 'output_price', 'context_window', 'is_multimodal', 'is_free']
    list_filter = ['company', 'is_multimodal', 'is_free', 'api_available']
    search_fields = ['name', 'company']

@admin.register(SubscriptionPlan)
class SubscriptionPlanAdmin(admin.ModelAdmin):
    list_display = ['model', 'name', 'price', 'is_free']
    list_filter = ['is_free', 'model']

@admin.register(Benchmark)
class BenchmarkAdmin(admin.ModelAdmin):
    list_display = ['model', 'benchmark_name', 'score', 'max_score']
    list_filter = ['benchmark_name']

@admin.register(PriceHistory)
class PriceHistoryAdmin(admin.ModelAdmin):
    list_display = ['model', 'date', 'input_price', 'output_price']

@admin.register(UserFavorite)
class UserFavoriteAdmin(admin.ModelAdmin):
    list_display = ['user', 'model', 'created_at']

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['user', 'model', 'rating', 'created_at']
    list_filter = ['rating']

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'bio']

@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ['user', 'message', 'is_read', 'created_at']
    list_filter = ['is_read']