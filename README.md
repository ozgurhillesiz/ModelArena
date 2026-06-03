## 🏗️ Teknik Mimari

### Veritabanı Tasarımı
Proje 10 ana model içermektedir:
- **AIModel**: AI model ve araçların tüm bilgileri (fiyat, benchmark, özellikler)
- **Review**: Kullanıcı yorumları ve 1-5 yıldız puanlama sistemi
- **UserFavorite**: Kullanıcı-model favori ilişkisi (unique_together ile tekrar engellendi)
- **ReviewLike**: Yorum beğeni sistemi
- **Benchmark**: Model performans test sonuçları
- **PriceHistory**: Fiyat geçmişi takibi
- **SubscriptionPlan**: Model abonelik planları
- **UserProfile**: Kullanıcı profil bilgileri (OneToOne ilişki)
- **Notification**: Kullanıcı bildirim sistemi
- **UserActivity**: Kullanıcı aktivite geçmişi
- **SecurityLog**: Güvenlik olayları kaydı

### İlişki Yapısı
- `Review` → `AIModel` (ForeignKey), `User` (ForeignKey), unique_together kısıtı
- `UserFavorite` → `User` + `AIModel` (unique_together ile çift favori engeli)
- `UserProfile` → `User` (OneToOneField, signal ile otomatik oluşturulur)
- `Benchmark` → `AIModel` (ForeignKey, related_name ile ORM sorguları)

### Mimari Kararlar
- **PostgreSQL**: Render'da kalıcı veri için SQLite yerine PostgreSQL tercih edildi
- **django-allauth**: Güvenli kimlik doğrulama, şifre sıfırlama ve oturum yönetimi
- **Django REST Framework**: `/api/models/`, `/api/benchmarks/`, `/api/price-history/` endpoint'leri
- **WhiteNoise**: Statik dosyalar için CDN'e gerek kalmadan verimli servis
- **Brevo API**: SMTP port kısıtlamalarını aşmak için HTTP API üzerinden email gönderimi
- **Cloudinary**: Medya dosyaları için bulut depolama altyapısı
- **CSP (Content Security Policy)**: XSS saldırılarına karşı header tabanlı koruma
- **select_related / prefetch_related**: N+1 sorgu problemini önlemek için ORM optimizasyonu

### Güvenlik Tasarımı
Uygulama çok katmanlı güvenlik mimarisi kullanmaktadır:
1. Kimlik doğrulama katmanı (allauth + güçlü şifre kuralları)
2. Yetkilendirme katmanı (@login_required, kullanıcıya özel veri erişimi)
3. Transport güvenliği (HTTPS zorlama, HSTS, güvenli cookie'ler)
4. İçerik güvenliği (CSP, XSS koruması, clickjacking önleme)
5. Brute force koruması (giriş denemesi sınırlama, güvenlik logları)
6. Veri minimizasyonu (yalnızca gerekli kişisel veriler toplanır)
