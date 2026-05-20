# 🤖 ModelArena

AI modellerini karşılaştır, fiyatları takip et, en iyisini seç.

## 📋 Proje Hakkında

ModelArena, yapay zeka modellerini (GPT-4o, Claude, Gemini, Llama vb.) karşılaştırmak, fiyatlarını takip etmek ve kullanım amacına göre en uygun modeli bulmak için geliştirilmiş bir Django web uygulamasıdır.

## ✨ Özellikler

- 🔍 **Model Arama & Filtreleme** — Şirkete, fiyata, özelliklere göre filtrele
- ⚡ **AJAX Arama** — Sayfa yenilenmeden anlık sonuçlar
- 📊 **Model Karşılaştırma** — Yan yana tablo ve grafik karşılaştırması
- 📈 **Benchmark Grafikleri** — MMLU, HumanEval, MATH skorları
- 💰 **Fiyat Geçmişi** — Zaman içindeki fiyat değişimleri
- 🔥 **Trending Modeller** — HuggingFace API'dan canlı veri
- 🤖 **Model Öneri Sistemi** — Kullanım amacına göre öneri
- ⭐ **Yorum & Puanlama** — Kullanıcı yorumları ve yıldız sistemi
- ❤️ **Favori Listesi** — Favori modellerini kaydet
- 👤 **Kullanıcı Profili** — Yorum ve favorileri takip et
- 🌙 **Dark/Light Mode** — Tema değiştirme
- 📱 **Responsive Tasarım** — Mobil uyumlu arayüz
- 🔐 **Email Doğrulama** — Güvenli kayıt sistemi
- 💱 **Canlı Döviz Kuru** — USD/TRY anlık kur
- 🚀 **REST API** — Django REST Framework ile API endpoints
- 💾 **Cache Sistemi** — Performans optimizasyonu

## 🛠️ Kullanılan Teknolojiler

- **Backend:** Django 5.2, Django REST Framework
- **Frontend:** Bootstrap 5, Chart.js, Vanilla JS
- **Veritabanı:** SQLite (geliştirme), PostgreSQL (production)
- **Email:** Brevo SMTP
- **API:** HuggingFace API, ExchangeRate API
- **Deployment:** Render

## 🚀 Kurulum

1. Repoyu klonla:
git clone https://github.com/kullanicin/modularena.git
cd modularena

2. Virtual environment oluştur:
python -m venv venv
venv\Scripts\activate

3. Paketleri yükle:
pip install -r requirements.txt

4. Veritabanını oluştur:
python manage.py migrate

5. Admin kullanıcı oluştur:
python manage.py createsuperuser

6. Sunucuyu başlat:
python manage.py runserver

## 🔑 Ortam Değişkenleri

SECRET_KEY=django-secret-key
EMAIL_HOST_USER=brevo-smtp-user
EMAIL_HOST_PASSWORD=brevo-smtp-password

## 📡 API Endpoints

| Endpoint | Açıklama |
|----------|----------|
| /api/models/ | Tüm AI modelleri |
| /api/models/search/?q=gpt | Model arama |
| /api/benchmarks/ | Benchmark verileri |
| /api/price-history/ | Fiyat geçmişi |

## 🧪 Testler

python manage.py test

## 📁 Proje Yapısı

ModelArena/
├── core/              # Django proje ayarları
├── models_app/        # Ana uygulama
│   ├── models.py      # Veritabanı modelleri
│   ├── views.py       # View fonksiyonları
│   ├── serializers.py # DRF serializers
│   ├── api_service.py # Harici API servisleri
│   └── tests.py       # Test dosyası
├── users/             # Kullanıcı yönetimi
├── templates/         # HTML şablonları
├── static/            # CSS, JS dosyaları
└── requirements.txt   # Python paketleri

## 👨‍💻 Geliştirici

Özgür Hillesiz