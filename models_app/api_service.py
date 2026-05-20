import requests

def fetch_huggingface_models(limit=10):
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
        return {'TRY': 38.0, 'EUR_TO_TRY': 41.5}
    except Exception as e:
        print(f"Döviz API Hatası: {e}")
        return {'TRY': 38.0, 'EUR_TO_TRY': 41.5}

def get_usd_to_try():
    rates = get_exchange_rates()
    return rates['TRY']

def fetch_ai_news(api_key):
    try:
        url = "https://newsapi.org/v2/everything"
        params = {
            'q': '"OpenAI" OR "Anthropic" OR "Google DeepMind" OR "ChatGPT" OR "Claude AI" OR "Gemini" OR "Meta AI"',
            'language': 'en',
            'sortBy': 'publishedAt',
            'pageSize': 12,
            'apiKey': api_key,
            'domains': 'techcrunch.com,theverge.com,wired.com,venturebeat.com,arstechnica.com'
        }
        response = requests.get(url, params=params, timeout=10)
        if response.status_code == 200:
            data = response.json()
            articles = data.get('articles', [])
            return [a for a in articles if a.get('url') and 'removed' not in a.get('title', '').lower()]
        return []
    except Exception as e:
        print(f"News API Hatası: {e}")
        return []