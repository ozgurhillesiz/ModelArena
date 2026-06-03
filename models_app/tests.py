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