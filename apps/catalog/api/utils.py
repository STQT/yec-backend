"""Утилиты для API"""

from django.conf import settings


def build_absolute_uri_https(request, url):
    """
    Строит абсолютный URL, в продакшне принудительно используя https.
    Решает проблему, когда request.build_absolute_uri возвращает http:// из-за
    прокси/балансировщика.
    """
    if not request or not url:
        return url
    uri = request.build_absolute_uri(url)
    if not settings.DEBUG and uri.startswith("http://"):
        uri = "https://" + uri[7:]
    return uri


def get_language_from_request(request):
    """
    Получает язык из query параметра lang.
    Если параметр не передан, возвращает язык по умолчанию (uz).
    
    Args:
        request: HTTP request объект
        
    Returns:
        str: Код языка ('uz', 'ru', или 'en')
        
    Examples:
        /api/carpets/?lang=ru  -> 'ru'
        /api/carpets/?lang=en  -> 'en'
        /api/carpets/          -> 'uz' (по умолчанию)
    """
    lang = request.query_params.get("lang", "uz").lower()
    
    # Проверяем, что язык поддерживается
    if lang not in ["uz", "ru", "en"]:
        return "uz"
    
    return lang
