"""
ModelArena - Test Dosyası
==========================
Temel unit ve integration testleri.
Modeller, view'lar ve kullanıcı işlemleri test edilir.
"""

from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from .models import AIModel, Review, UserFavorite, Benchmark, UserProfile


class AIModelTestCase(TestCase):
    """AIModel modeli için unit testler."""

    def setUp(self):
        """Her test öncesi örnek veri oluşturur."""
        self.model = AIModel.objects.create(
            name='GPT-4',
            company='OpenAI',
            category='model',
            input_price=0.00003,
            output_price=0.00006,
            context_window=128000,
            is_multimodal=True,
            is_free=False,
            api_available=True,
        )

    def test_model_created(self):
        """Model doğru oluşturuldu mu?"""
        self.assertEqual(self.model.name, 'GPT-4')
        self.assertEqual(self.model.company, 'OpenAI')

    def test_model_str(self):
        """__str__ metodu doğru çalışıyor mu?"""
        self.assertEqual(str(self.model), 'OpenAI - GPT-4')

    def test_input_price_per_million(self):
        """1 milyon token fiyatı doğru hesaplanıyor mu?"""
        self.assertEqual(self.model.input_price_per_million, 30.0)

    def test_output_price_per_million(self):
        """Output fiyatı doğru hesaplanıyor mu?"""
        self.assertEqual(self.model.output_price_per_million, 60.0)

    def test_average_rating_no_reviews(self):
        """Yorum yokken ortalama puan 0 olmalı."""
        self.assertEqual(self.model.average_rating, 0)

    def test_strengths_list(self):
        """Güçlü yönler virgülle ayrılıp liste döndürülüyor mu?"""
        self.model.strengths = 'Hızlı, Güvenilir, Çok dilli'
        self.model.save()
        self.assertEqual(len(self.model.strengths_list), 3)


class ReviewTestCase(TestCase):
    """Review modeli için unit testler."""

    def setUp(self):
        """Test kullanıcısı ve modeli oluşturur."""
        self.user = User.objects.create_user(
            username='testuser',
            password='Test1234!',
            email='test@test.com'
        )
        self.ai_model = AIModel.objects.create(
            name='Claude',
            company='Anthropic',
            category='model',
        )

    def test_review_created(self):
        """Yorum doğru oluşturuluyor mu?"""
        review = Review.objects.create(
            user=self.user,
            model=self.ai_model,
            rating=5,
            comment='Harika bir model!'
        )
        self.assertEqual(review.rating, 5)
        self.assertEqual(review.comment, 'Harika bir model!')

    def test_average_rating_with_review(self):
        """Yorum eklendikten sonra ortalama puan hesaplanıyor mu?"""
        Review.objects.create(
            user=self.user,
            model=self.ai_model,
            rating=4,
            comment='İyi model.'
        )
        self.assertEqual(self.ai_model.average_rating, 4.0)

    def test_review_unique_together(self):
        """Aynı kullanıcı aynı modele iki yorum yapamamalı."""
        Review.objects.create(
            user=self.user,
            model=self.ai_model,
            rating=5,
            comment='İlk yorum'
        )
        from django.db import IntegrityError
        with self.assertRaises(IntegrityError):
            Review.objects.create(
                user=self.user,
                model=self.ai_model,
                rating=3,
                comment='İkinci yorum'
            )


class UserFavoriteTestCase(TestCase):
    """UserFavorite modeli için unit testler."""

    def setUp(self):
        self.user = User.objects.create_user(
            username='favuser',
            password='Test1234!',
        )
        self.ai_model = AIModel.objects.create(
            name='Gemini',
            company='Google',
            category='model',
        )

    def test_favorite_created(self):
        """Favori doğru oluşturuluyor mu?"""
        fav = UserFavorite.objects.create(
            user=self.user,
            model=self.ai_model
        )
        self.assertEqual(fav.user, self.user)
        self.assertEqual(fav.model, self.ai_model)

    def test_favorite_unique_together(self):
        """Aynı kullanıcı aynı modeli iki kez favoriye ekleyememeli."""
        UserFavorite.objects.create(user=self.user, model=self.ai_model)
        from django.db import IntegrityError
        with self.assertRaises(IntegrityError):
            UserFavorite.objects.create(user=self.user, model=self.ai_model)


class UserProfileTestCase(TestCase):
    """UserProfile signal testi."""

    def test_profile_auto_created(self):
        """Kullanıcı oluşturunca profil otomatik oluşuyor mu?"""
        user = User.objects.create_user(
            username='profileuser',
            password='Test1234!',
        )
        self.assertTrue(UserProfile.objects.filter(user=user).exists())


class ViewTestCase(TestCase):
    """Temel view integration testleri."""

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='viewuser',
            password='Test1234!',
        )
        self.ai_model = AIModel.objects.create(
            name='DeepSeek',
            company='DeepSeek',
            category='model',
        )

    def test_home_page(self):
        """Ana sayfa 200 döndürüyor mu?"""
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)

    def test_model_detail_page(self):
        """Model detay sayfası 200 döndürüyor mu?"""
        response = self.client.get(reverse('model_detail', args=[self.ai_model.pk]))
        self.assertEqual(response.status_code, 200)

    def test_profile_redirect_if_not_logged_in(self):
        """Giriş yapmadan profile girilince login'e yönlendiriyor mu?"""
        response = self.client.get(reverse('profile'))
        self.assertEqual(response.status_code, 302)

    def test_profile_accessible_when_logged_in(self):
        """Giriş yapılınca profil sayfası açılıyor mu?"""
        self.client.login(username='viewuser', password='Test1234!')
        response = self.client.get(reverse('profile'))
        self.assertEqual(response.status_code, 200)

    def test_toggle_favorite_requires_login(self):
        """Giriş yapmadan favori eklenemez mi?"""
        response = self.client.get(reverse('toggle_favorite', args=[self.ai_model.pk]))
        self.assertEqual(response.status_code, 302)


class AIModelFilterTestCase(TestCase):
    """AIModel filtreleme ve arama testleri."""

    def setUp(self):
        self.model1 = AIModel.objects.create(
            name='GPT-4', company='OpenAI', category='model',
            is_free=False, is_multimodal=True, input_price=0.00003
        )
        self.model2 = AIModel.objects.create(
            name='Llama', company='Meta', category='model',
            is_free=True, is_multimodal=False, input_price=0.0
        )
        self.tool = AIModel.objects.create(
            name='Midjourney', company='Midjourney', category='tool',
            is_free=False
        )

    def test_filter_by_category_model(self):
        """Model kategorisi filtresi calisiyor mu?"""
        models = AIModel.objects.filter(category='model')
        self.assertEqual(models.count(), 2)

    def test_filter_by_category_tool(self):
        """Tool kategorisi filtresi calisiyor mu?"""
        tools = AIModel.objects.filter(category='tool')
        self.assertEqual(tools.count(), 1)

    def test_filter_free_models(self):
        """Ucretsiz model filtresi calisiyor mu?"""
        free = AIModel.objects.filter(is_free=True)
        self.assertEqual(free.count(), 1)
        self.assertEqual(free.first().name, 'Llama')

    def test_filter_multimodal(self):
        """Multimodal filtresi calisiyor mu?"""
        multimodal = AIModel.objects.filter(is_multimodal=True)
        self.assertEqual(multimodal.count(), 1)

    def test_search_by_name(self):
        """Model adi ile arama calisiyor mu?"""
        from django.db.models import Q
        results = AIModel.objects.filter(Q(name__icontains='gpt'))
        self.assertEqual(results.count(), 1)

    def test_search_by_company(self):
        """Sirket adi ile arama calisiyor mu?"""
        from django.db.models import Q
        results = AIModel.objects.filter(Q(company__icontains='meta'))
        self.assertEqual(results.count(), 1)

    def test_model_count(self):
        """Toplam model sayisi dogru mu?"""
        self.assertEqual(AIModel.objects.count(), 3)

    def test_weaknesses_list_empty(self):
        """Bos weaknesses listesi bos liste donduruyor mu?"""
        self.assertEqual(self.model1.weaknesses_list, [])

    def test_review_count_zero(self):
        """Yorumsuz modelin yorum sayisi 0 mi?"""
        self.assertEqual(self.model1.review_count, 0)


class BenchmarkTestCase(TestCase):
    """Benchmark modeli testleri."""

    def setUp(self):
        self.model = AIModel.objects.create(
            name='Claude', company='Anthropic', category='model'
        )

    def test_benchmark_created(self):
        """Benchmark dogru olusturuluyor mu?"""
        bench = Benchmark.objects.create(
            model=self.model,
            benchmark_name='MMLU',
            score=88.5,
            max_score=100
        )
        self.assertEqual(bench.score, 88.5)
        self.assertEqual(bench.benchmark_name, 'MMLU')

    def test_benchmark_str(self):
        """Benchmark __str__ metodu calisiyor mu?"""
        bench = Benchmark.objects.create(
            model=self.model,
            benchmark_name='HumanEval',
            score=75.0
        )
        self.assertIn('HumanEval', str(bench))

    def test_multiple_benchmarks(self):
        """Bir modele birden fazla benchmark eklenebiliyor mu?"""
        Benchmark.objects.create(model=self.model, benchmark_name='MMLU', score=88.0)
        Benchmark.objects.create(model=self.model, benchmark_name='HumanEval', score=75.0)
        self.assertEqual(self.model.benchmarks.count(), 2)


class PriceHistoryTestCase(TestCase):
    """PriceHistory modeli testleri."""

    def setUp(self):
        self.model = AIModel.objects.create(
            name='GPT-3.5', company='OpenAI', category='model'
        )

    def test_price_history_created(self):
        """Fiyat gecmisi dogru olusturuluyor mu?"""
        from .models import PriceHistory
        from datetime import date
        ph = PriceHistory.objects.create(
            model=self.model,
            date=date(2024, 1, 1),
            input_price=0.000002,
            output_price=0.000002
        )
        self.assertEqual(ph.input_price, 0.000002)

    def test_price_history_str(self):
        """PriceHistory __str__ calisiyor mu?"""
        from .models import PriceHistory
        from datetime import date
        ph = PriceHistory.objects.create(
            model=self.model,
            date=date(2024, 1, 1),
            input_price=0.000002,
            output_price=0.000002
        )
        self.assertIn('GPT-3.5', str(ph))


class NotificationTestCase(TestCase):
    """Notification modeli testleri."""

    def setUp(self):
        self.user = User.objects.create_user(
            username='notifuser', password='Test1234!'
        )

    def test_notification_created(self):
        """Bildirim dogru olusturuluyor mu?"""
        from .models import Notification
        notif = Notification.objects.create(
            user=self.user,
            message='Test bildirimi'
        )
        self.assertEqual(notif.is_read, False)
        self.assertEqual(notif.message, 'Test bildirimi')

    def test_notification_mark_read(self):
        """Bildirim okundu olarak isaretleniyor mu?"""
        from .models import Notification
        notif = Notification.objects.create(
            user=self.user, message='Test'
        )
        notif.is_read = True
        notif.save()
        updated = Notification.objects.get(pk=notif.pk)
        self.assertTrue(updated.is_read)

    def test_unread_count(self):
        """Okunmamis bildirim sayisi dogru hesaplaniyor mu?"""
        from .models import Notification
        # Onceki bildirimleri temizle (signal ile gelen hosgeldin bildirimi)
        Notification.objects.filter(user=self.user).delete()
        Notification.objects.create(user=self.user, message='Bildirim 1')
        Notification.objects.create(user=self.user, message='Bildirim 2')
        count = Notification.objects.filter(user=self.user, is_read=False).count()
        self.assertEqual(count, 2)


class SecurityLogTestCase(TestCase):
    """SecurityLog modeli testleri."""

    def test_security_log_created(self):
        """Guvenlik logu dogru olusturuluyor mu?"""
        from .models import SecurityLog
        log = SecurityLog.objects.create(
            ip_address='127.0.0.1',
            username='testuser',
            action='login_failed',
            success=False
        )
        self.assertEqual(log.action, 'login_failed')
        self.assertFalse(log.success)

    def test_security_log_success(self):
        """Basarili giris logu dogru kaydediliyor mu?"""
        from .models import SecurityLog
        log = SecurityLog.objects.create(
            ip_address='127.0.0.1',
            username='testuser',
            action='login_success',
            success=True
        )
        self.assertTrue(log.success)

    def test_failed_attempts_count(self):
        """Basarisiz deneme sayisi dogru sayiliyor mu?"""
        from .models import SecurityLog
        SecurityLog.objects.create(ip_address='10.0.0.1', username='hacker', action='login_failed', success=False)
        SecurityLog.objects.create(ip_address='10.0.0.1', username='hacker', action='login_failed', success=False)
        SecurityLog.objects.create(ip_address='10.0.0.1', username='hacker', action='login_failed', success=False)
        count = SecurityLog.objects.filter(ip_address='10.0.0.1', action='login_failed').count()
        self.assertEqual(count, 3)


class UserActivityTestCase(TestCase):
    """UserActivity modeli testleri."""

    def setUp(self):
        self.user = User.objects.create_user(
            username='activityuser', password='Test1234!'
        )
        self.model = AIModel.objects.create(
            name='Gemini', company='Google', category='model'
        )

    def test_activity_created(self):
        """Aktivite dogru olusturuluyor mu?"""
        from .models import UserActivity
        activity = UserActivity.objects.create(
            user=self.user,
            activity_type='review',
            model=self.model,
            description='Test aktivite'
        )
        self.assertEqual(activity.activity_type, 'review')

    def test_activity_types(self):
        """Tum aktivite tipleri olusturulabiliyor mu?"""
        from .models import UserActivity
        types = ['review', 'favorite', 'unfavorite', 'compare', 'recommend']
        for t in types:
            UserActivity.objects.create(
                user=self.user, activity_type=t, model=self.model
            )
        self.assertEqual(UserActivity.objects.filter(user=self.user).count(), 5)


class MoreViewTestCase(TestCase):
    """Ek view integration testleri."""

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='moreviewuser', password='Test1234!'
        )
        self.model = AIModel.objects.create(
            name='TestModel', company='TestCo', category='model'
        )

    def test_tools_page(self):
        """Araclar sayfasi 200 donduruyor mu?"""
        response = self.client.get(reverse('tools'))
        self.assertEqual(response.status_code, 200)

    def test_compare_page(self):
        """Karsilastirma sayfasi 200 donduruyor mu?"""
        response = self.client.get(reverse('compare'))
        self.assertEqual(response.status_code, 200)

    def test_stats_page(self):
        """Istatistik sayfasi 200 donduruyor mu?"""
        response = self.client.get(reverse('stats'))
        self.assertEqual(response.status_code, 200)

    def test_recommend_page(self):
        """Oneri sayfasi 200 donduruyor mu?"""
        response = self.client.get(reverse('recommend'))
        self.assertEqual(response.status_code, 200)

    def test_add_review_requires_login(self):
        """Giris yapmadan yorum eklenemez mi?"""
        response = self.client.post(reverse('add_review', args=[self.model.pk]))
        self.assertEqual(response.status_code, 302)

    def test_delete_review_requires_login(self):
        """Giris yapmadan yorum silinemez mi?"""
        response = self.client.post(reverse('delete_review', args=[1]))
        self.assertEqual(response.status_code, 302)

    def test_favorites_requires_login(self):
        """Giris yapmadan favoriler acilmiyor mu?"""
        response = self.client.get(reverse('favorites'))
        self.assertEqual(response.status_code, 302)

    def test_model_detail_with_review(self):
        """Yorumlu model detay sayfasi calisiyor mu?"""
        Review.objects.create(
            user=self.user, model=self.model, rating=5, comment='Harika'
        )
        response = self.client.get(reverse('model_detail', args=[self.model.pk]))
        self.assertEqual(response.status_code, 200)

    def test_home_with_search(self):
        """Arama parametresiyle ana sayfa calisiyor mu?"""
        response = self.client.get(reverse('home') + '?search=test')
        self.assertEqual(response.status_code, 200)

    def test_home_with_filter(self):
        """Filtre parametresiyle ana sayfa calisiyor mu?"""
        response = self.client.get(reverse('home') + '?is_free=1')
        self.assertEqual(response.status_code, 200)