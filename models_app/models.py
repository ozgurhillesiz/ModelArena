from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.conf import settings

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)
    bio = models.TextField(blank=True)

    def __str__(self):
        return f"{self.user.username} profili"

class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    link = models.URLField(blank=True)

    def __str__(self):
        return f"{self.user.username} - {self.message[:50]}"

class UserActivity(models.Model):
    ACTIVITY_TYPES = [
        ('review', 'Yorum Yapıldı'),
        ('favorite', 'Favoriye Eklendi'),
        ('unfavorite', 'Favoriden Çıkarıldı'),
        ('compare', 'Karşılaştırıldı'),
        ('recommend', 'Öneri Gönderildi'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='activities')
    activity_type = models.CharField(max_length=20, choices=ACTIVITY_TYPES)
    model = models.ForeignKey('AIModel', on_delete=models.CASCADE, null=True, blank=True)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.username} - {self.activity_type}"

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)
        Notification.objects.create(
            user=instance,
            message=f'🎉 Hoş geldin {instance.username}! ModelArena\'ya katıldığın için teşekkürler. AI modellerini keşfetmeye başla!',
            link='/'
        )
        try:
            send_mail(
                subject=f'🆕 Yeni Kullanıcı: {instance.username}',
                message=f'ModelArena\'ya yeni bir kullanıcı kayıt oldu!\n\nKullanıcı adı: {instance.username}\nEmail: {instance.email}\nTarih: {instance.date_joined}',
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=['ozgurhillesiz@outlook.com'],
                fail_silently=True,
            )
        except:
            pass

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    try:
        instance.profile.save()
    except UserProfile.DoesNotExist:
        UserProfile.objects.create(user=instance)

class AIModel(models.Model):
    CATEGORY_CHOICES = [
        ('model', 'AI Model'),
        ('tool', 'AI Araç'),
    ]
    name = models.CharField(max_length=200)
    company = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    input_price = models.DecimalField(max_digits=10, decimal_places=6, null=True, blank=True)
    output_price = models.DecimalField(max_digits=10, decimal_places=6, null=True, blank=True)
    context_window = models.IntegerField(null=True, blank=True)
    release_date = models.DateField(null=True, blank=True)
    is_multimodal = models.BooleanField(default=False)
    is_free = models.BooleanField(default=False)
    api_available = models.BooleanField(default=True)
    image_url = models.URLField(blank=True)
    subscription_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    subscription_name = models.CharField(max_length=200, blank=True)
    website_url = models.URLField(blank=True)
    parameters = models.CharField(max_length=50, blank=True)
    strengths = models.TextField(blank=True, help_text="Her maddeyi virgülle ayır")
    weaknesses = models.TextField(blank=True, help_text="Her maddeyi virgülle ayır")
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='model')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.company} - {self.name}"

    @property
    def input_price_per_million(self):
        if self.input_price:
            return round(float(self.input_price) * 1_000_000, 2)
        return 0

    @property
    def output_price_per_million(self):
        if self.output_price:
            return round(float(self.output_price) * 1_000_000, 2)
        return 0

    @property
    def average_rating(self):
        reviews = self.reviews.all()
        if reviews:
            return round(sum(r.rating for r in reviews) / len(reviews), 1)
        return 0

    @property
    def review_count(self):
        return self.reviews.count()

    @property
    def strengths_list(self):
        return [s.strip() for s in self.strengths.split(',') if s.strip()]

    @property
    def weaknesses_list(self):
        return [w.strip() for w in self.weaknesses.split(',') if w.strip()]

class SubscriptionPlan(models.Model):
    model = models.ForeignKey(AIModel, on_delete=models.CASCADE, related_name='plans')
    name = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    features = models.TextField(blank=True, help_text="Her özelliği virgülle ayır")
    is_free = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.model.name} - {self.name}"

    @property
    def feature_list(self):
        return [f.strip() for f in self.features.split(',') if f.strip()]

class Benchmark(models.Model):
    model = models.ForeignKey(AIModel, on_delete=models.CASCADE, related_name='benchmarks')
    benchmark_name = models.CharField(max_length=200)
    score = models.FloatField()
    max_score = models.FloatField(default=100)
    source_url = models.URLField(blank=True)

    def __str__(self):
        return f"{self.model.name} - {self.benchmark_name}"

class PriceHistory(models.Model):
    model = models.ForeignKey(AIModel, on_delete=models.CASCADE, related_name='price_history')
    date = models.DateField()
    input_price = models.DecimalField(max_digits=10, decimal_places=6)
    output_price = models.DecimalField(max_digits=10, decimal_places=6)

    def __str__(self):
        return f"{self.model.name} - {self.date}"

class UserFavorite(models.Model):
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    model = models.ForeignKey(AIModel, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'model')

    def __str__(self):
        return f"{self.user.username} - {self.model.name}"

class Review(models.Model):
    model = models.ForeignKey(AIModel, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    rating = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'model')

    def __str__(self):
        return f"{self.user.username} - {self.model.name} - {self.rating}"


class ReviewLike(models.Model):
    review = models.ForeignKey(Review, on_delete=models.CASCADE, related_name='likes')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('review', 'user')

    def __str__(self):
        return f"{self.user.username} - {self.review.pk}"