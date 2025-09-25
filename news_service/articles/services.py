import requests
from django.conf import settings

NEWS_API_URL = "https://newsapi.org/v2/top-headlines"

def fetch_articles_from_api():
    params = {
        "country": "us",
        "apiKey": settings.NEWS_API_KEY,
        "pageSize": 20,
    }
    response = requests.get(NEWS_API_URL, params=params)
    response.raise_for_status()
    return response.json().get("articles", [])
