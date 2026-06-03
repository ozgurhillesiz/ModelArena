from django.contrib import admin
from django.utils.html import format_html
from .models import AIModel, Benchmark, PriceHistory, UserFavorite, Review, SubscriptionPlan, UserProfile, Notification, SecurityLog, UserActivity, ReviewLike

admin.site.site_header = "ModelArena Yönetim Paneli"
admin.site.site_title = "ModelArena Admin"
admin.site.index_title = "Yönetim Paneline Hoş Geldiniz"

@admin.register(AIModel)
class AIModelAdmin(admin.ModelAdmin):
    list_display = ['name', 'company', 'category', 'input_price', 'output_price', 'context_window', 'is_multimodal', 'is_free']
    list_filter = ['company', 'is_multimodal', 'is_free', 'api_available', 'category']
    search_fields = ['name', 'company']

    fieldsets = (
        ('Temel Bilgiler', {
            'fields': ('name', 'company', 'category', 'description', 'image_url', 'website_url')
        }),
        ('Fiyatlandırma', {
            'fields': ('input_price', 'output_price', 'subscription_name', 'subscription_price'),
            'description': 'API token fiyatları ve abonelik bilgileri'
        }),
        ('Teknik Özellikler', {
            'fields': ('context_window', 'parameters', 'release_date', 'is_multimodal', 'is_free', 'api_available')
        }),
        ('Güçlü & Zayıf Yönler', {
            'fields': ('strengths', 'weaknesses'),
            'description': 'Her maddeyi virgülle ayırın'
        }),
    )

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
    list_display = ['favori_ikon', 'user', 'model', 'created_at']
    list_filter = ['model']
    search_fields = ['user__username']

    @admin.display(description='')
    def favori_ikon(self, obj):
        return format_html('<span style="color:#f59e0b;font-size:1.1rem;">★</span>')

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['yorum_ikon', 'user', 'model', 'rating', 'created_at']
    list_filter = ['rating']
    search_fields = ['user__username']

    @admin.display(description='')
    def yorum_ikon(self, obj):
        return format_html('<span style="color:#6c63ff;font-size:1.1rem;">💬</span>')

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