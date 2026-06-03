"""
ModelArena - Üçüncü Parti API Servisleri
==========================================
HuggingFace, ExchangeRate ve NewsAPI entegrasyonlarını içerir.
Tüm fonksiyonlar timeout ve hata yönetimi ile korunmuştur.
Sonuçlar view katmanında önbelleğe (cache) alınır.
"""

import requests


def fetch_huggingface_models(limit=10):
    """
    HuggingFace API'den en çok indirilen text-generation modellerini çeker.
    Hata durumunda boş liste döndürür.
    """
    url = "https://huggingface.co/api/models"
    params = {
        'limit': limit,
        'sort': 'downloads',
        'direction': -1,
        'filter': 'text-generation'
    }
    try:
        response = requests.get(url, params=params, timeout=10)
        if response.status_code == 200:
            return response.json()
        return []
    except Exception as e:
        print(f"API Hatası: {e}")
        return []


def get_model_stats(model_id):
    """
    HuggingFace'den belirli bir modelin detay bilgilerini çeker.
    Hata durumunda None döndürür.
    """
    url = f"https://huggingface.co/api/models/{model_id}"
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            return response.json()
        return None
    except Exception as e:
        print(f"API Hatası: {e}")
        return None


def get_exchange_rates():
    """
    ExchangeRate API'den güncel USD/TRY ve EUR/TRY kurlarını çeker.
    API erişilemezse varsayılan değerler döndürür.
    """
    try:
        url = "https://api.exchangerate-api.com/v4/latest/USD"
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            data = response.json()
            usd_to_try = round(data['rates']['TRY'], 2)
            eur_to_try = round(data['rates']['TRY'] / data['rates']['EUR'], 2)
            return {
                'TRY': usd_to_try,
                'EUR_TO_TRY': eur_to_try,
            }
        # API erişilemezse varsayılan kur değerleri
        return {'TRY': 38.0, 'EUR_TO_TRY': 41.5}
    except Exception as e:
        print(f"Döviz API Hatası: {e}")
        return {'TRY': 38.0, 'EUR_TO_TRY': 41.5}


def get_usd_to_try():
    """Sadece USD/TRY kurunu döndüren yardımcı fonksiyon."""
    rates = get_exchange_rates()
    return rates['TRY']


def fetch_ai_news(api_key):
    """
    NewsAPI'den güncel AI haberlerini çeker.
    Güvenilir teknoloji kaynaklarından (TechCrunch, Wired vb.) filtreler.
    Kaldırılmış/eksik haberleri temizler.
    """
    try:
        url = "https://newsapi.org/v2/everything"
        params = {
            'q': '"OpenAI" OR "Anthropic" OR "Google DeepMind" OR "ChatGPT" OR "Claude AI" OR "Gemini" OR "Meta AI"',
            'language': 'en',
            'sortBy': 'publishedAt',
            'pageSize': 12,
            'apiKey': api_key,
            # Güvenilir AI/teknoloji haber kaynakları
            'domains': 'techcrunch.com,theverge.com,wired.com,venturebeat.com,arstechnica.com'
        }
        response = requests.get(url, params=params, timeout=10)
        if response.status_code == 200:
            data = response.json()
            articles = data.get('articles', [])
            # URL'si olmayan veya kaldırılmış haberleri filtrele
            return [a for a in articles if a.get('url') and 'removed' not in a.get('title', '').lower()]
        return []
    except Exception as e:
        print(f"News API Hatası: {e}")
        return []