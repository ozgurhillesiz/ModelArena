from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'models', views.AIModelViewSet)
router.register(r'benchmarks', views.BenchmarkViewSet)
router.register(r'price-history', views.PriceHistoryViewSet)

urlpatterns = [
    path('', views.home, name='home'),
    path('model/<int:pk>/', views.model_detail, name='model_detail'),
    path('model/<int:pk>/favorite/', views.toggle_favorite, name='toggle_favorite'),
    path('model/<int:pk>/review/', views.add_review, name='add_review'),
    path('model/<int:pk>/recommend/', views.recommend_model, name='recommend_model'),
    path('review/<int:pk>/delete/', views.delete_review, name='delete_review'),
    path('compare/', views.compare, name='compare'),
    path('favorites/', views.favorites, name='favorites'),
    path('trending/', views.trending, name='trending'),
    path('trending/<path:model_id>/', views.model_hf_detail, name='model_hf_detail'),
    path('news/', views.news, name='news'),
    path('recommend/', views.recommend, name='recommend'),
    path('stats/', views.stats, name='stats'),
    path('api/', include(router.urls)),
]