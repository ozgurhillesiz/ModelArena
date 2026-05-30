from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from users import views as user_views

urlpatterns = [
    path('gizli-admin-ma2026/', admin.site.urls),
    path('', include('models_app.urls')),
    path('users/', include('users.urls')),
    path('accounts/password/reset/', user_views.custom_password_reset, name='account_reset_password'),
    path('accounts/', include('allauth.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)