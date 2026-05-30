from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.profile_view, name='profile'),
    path('delete-account/', views.delete_account, name='delete_account'),
    path('notification/<int:pk>/read/', views.mark_notification_read, name='mark_notification_read'),
    path('notifications/read-all/', views.mark_all_read, name='mark_all_read'),
    path('notifications/count/', views.notification_count, name='notification_count'),
]