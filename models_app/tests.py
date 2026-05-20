from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from .models import AIModel, Benchmark, PriceHistory, UserFavorite, Review
from datetime import date

class AIModelTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123',
            email='test@test.com'
        )
        self.model = AIModel.objects.create(
            name='Test GPT',
            company='Test AI',
            description='Test description',
            input_price=0.000005,
            output_price=0.000015,
            context_window=128,
            release_date=date(2024, 1, 1),
            is_multimodal=True,
            is_free=False,
            api_available=True,
        )

    def test_home_page(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)

    def test_model_detail_page(self):
        response = self.client.get(reverse('model_detail', args=[self.model.pk]))
        self.assertEqual(response.status_code, 200)

    def test_compare_page(self):
        response = self.client.get(reverse('compare'))
        self.assertEqual(response.status_code, 200)

    def test_trending_page(self):
        response = self.client.get(reverse('trending'))
        self.assertEqual(response.status_code, 200)

    def test_recommend_page(self):
        response = self.client.get(reverse('recommend'))
        self.assertEqual(response.status_code, 200)

    def test_input_price_per_million(self):
        self.assertEqual(self.model.input_price_per_million, 5.0)

    def test_output_price_per_million(self):
        self.assertEqual(self.model.output_price_per_million, 15.0)

    def test_average_rating_no_reviews(self):
        self.assertEqual(self.model.average_rating, 0)

    def test_review_count_no_reviews(self):
        self.assertEqual(self.model.review_count, 0)

    def test_add_review(self):
        self.client.login(username='testuser', password='testpass123')
        Review.objects.create(
            user=self.user,
            model=self.model,
            rating=5,
            comment='Harika model!'
        )
        self.assertEqual(self.model.review_count, 1)
        self.assertEqual(self.model.average_rating, 5.0)

    def test_favorite_toggle(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('toggle_favorite', args=[self.model.pk]))
        self.assertEqual(UserFavorite.objects.filter(user=self.user, model=self.model).count(), 1)

    def test_search_filter(self):
        response = self.client.get(reverse('home') + '?search=Test')
        self.assertEqual(response.status_code, 200)

    def test_company_filter(self):
        response = self.client.get(reverse('home') + '?company=Test AI')
        self.assertEqual(response.status_code, 200)

    def test_api_models_endpoint(self):
        response = self.client.get('/api/models/')
        self.assertEqual(response.status_code, 200)

    def test_api_benchmarks_endpoint(self):
        response = self.client.get('/api/benchmarks/')
        self.assertEqual(response.status_code, 200)

    def test_favorites_requires_login(self):
        response = self.client.get(reverse('favorites'))
        self.assertEqual(response.status_code, 302)

    def test_profile_requires_login(self):
        response = self.client.get(reverse('profile'))
        self.assertEqual(response.status_code, 302)