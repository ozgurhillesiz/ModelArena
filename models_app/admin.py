from django.contrib import admin
from .models import AIModel, Benchmark, PriceHistory, UserFavorite, Review, SubscriptionPlan, UserProfile, Notification, SecurityLog, UserActivity, ReviewLike

@admin.register(AIModel)
class AIModelAdmin(admin.ModelAdmin):
    list_display = ['name', 'company', 'input_price', 'output_price', 'context_window', 'is_multimodal', 'is_free', 'category']
    list_filter = ['company', 'is_multimodal', 'is_free', 'api_available', 'category']
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

@admin.register(ReviewLike)
class ReviewLikeAdmin(admin.ModelAdmin):
    list_display = ['user', 'review', 'created_at']

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'bio']

@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ['user', 'message', 'is_read', 'created_at']
    list_filter = ['is_read']

@admin.register(UserActivity)
class UserActivityAdmin(admin.ModelAdmin):
    list_display = ['user', 'activity_type', 'model', 'created_at']
    list_filter = ['activity_type']
    search_fields = ['user__username']

@admin.register(SecurityLog)
class SecurityLogAdmin(admin.ModelAdmin):
    list_display = ['ip_address', 'username', 'action', 'success', 'created_at']
    list_filter = ['action', 'success']
    search_fields = ['ip_address', 'username']
    readonly_fields = ['ip_address', 'username', 'action', 'success', 'created_at']