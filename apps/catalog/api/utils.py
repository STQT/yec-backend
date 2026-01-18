"""Утилиты для API"""


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
