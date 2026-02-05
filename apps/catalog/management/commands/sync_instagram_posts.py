"""
Management команда для синхронизации постов из Instagram

Использование:
    python manage.py sync_instagram_posts

Для работы требуется:
    1. Instagram Business или Creator аккаунт
    2. Facebook App с подключенным Instagram
    3. Access Token с правами instagram_basic, pages_read_engagement

Альтернативный способ (без официального API):
    Можно использовать библиотеку instagrapi (неофициальная)
    или парсинг (не рекомендуется из-за ToS)
"""

import requests
from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
from django.utils import timezone
from apps.catalog.models import InstagramPost


class Command(BaseCommand):
    help = 'Синхронизирует посты из Instagram через Instagram Graph API'

    def add_arguments(self, parser):
        parser.add_argument(
            '--limit',
            type=int,
            default=12,
            help='Количество постов для получения (по умолчанию: 12, 0 = все доступные)',
        )
        parser.add_argument(
            '--username',
            type=str,
            help='Instagram username (по умолчанию из настроек)',
        )
        parser.add_argument(
            '--all',
            action='store_true',
            help='Получить все доступные посты (эквивалентно --limit 0)',
        )

    def handle(self, *args, **options):
        limit = 0 if options.get('all') else options['limit']
        username = options.get('username') or getattr(settings, 'INSTAGRAM_USERNAME', 'yecgilam')
        
        # Получаем настройки из settings
        access_token = getattr(settings, 'INSTAGRAM_ACCESS_TOKEN', None)
        instagram_business_account_id = getattr(settings, 'INSTAGRAM_BUSINESS_ACCOUNT_ID', None)
        
        if not access_token:
            self.stdout.write(
                self.style.ERROR(
                    'INSTAGRAM_ACCESS_TOKEN не настроен в settings.\n'
                    'Добавьте его в config/settings/base.py или .env файл.'
                )
            )
            return
        
        if not instagram_business_account_id:
            self.stdout.write(
                self.style.ERROR(
                    'INSTAGRAM_BUSINESS_ACCOUNT_ID не настроен в settings.\n'
                    'Добавьте его в config/settings/base.py или .env файл.'
                )
            )
            return
        
        try:
            # Получаем посты через Instagram Graph API
            posts = self.fetch_instagram_posts(
                instagram_business_account_id,
                access_token,
                limit
            )
            
            if not posts:
                self.stdout.write(
                    self.style.WARNING('Не удалось получить посты из Instagram')
                )
                return
            
            # Сохраняем посты в базу данных
            created_count = 0
            updated_count = 0
            
            for post_data in posts:
                instagram_id = post_data.get('id')
                if not instagram_id:
                    continue
                
                # Определяем тип поста
                media_type = post_data.get('media_type', 'IMAGE').upper()
                if media_type == 'IMAGE':
                    post_type = 'IMAGE'
                elif media_type == 'VIDEO':
                    post_type = 'VIDEO'
                elif media_type == 'CAROUSEL_ALBUM':
                    post_type = 'CAROUSEL_ALBUM'
                else:
                    post_type = 'IMAGE'
                
                # Получаем URL медиа
                media_url = post_data.get('media_url') or post_data.get('thumbnail_url')
                
                # Парсим timestamp
                timestamp_str = post_data.get('timestamp')
                if timestamp_str:
                    from datetime import datetime
                    timestamp = datetime.fromisoformat(timestamp_str.replace('Z', '+00:00'))
                else:
                    timestamp = timezone.now()
                
                # Создаем или обновляем пост
                post, created = InstagramPost.objects.update_or_create(
                    instagram_id=instagram_id,
                    defaults={
                        'post_type': post_type,
                        'caption': post_data.get('caption', '')[:5000] if post_data.get('caption') else None,
                        'permalink': post_data.get('permalink', ''),
                        'thumbnail_url': post_data.get('thumbnail_url', ''),
                        'media_url': media_url,
                        'like_count': post_data.get('like_count', 0),
                        'comments_count': post_data.get('comments_count', 0),
                        'timestamp': timestamp,
                    }
                )
                
                if created:
                    created_count += 1
                else:
                    updated_count += 1
            
            self.stdout.write(
                self.style.SUCCESS(
                    f'Успешно синхронизировано постов:\n'
                    f'  Создано: {created_count}\n'
                    f'  Обновлено: {updated_count}\n'
                    f'  Всего обработано: {len(posts)}'
                )
            )
            
        except Exception as e:
            raise CommandError(f'Ошибка при синхронизации: {str(e)}')

    def fetch_instagram_posts(self, account_id, access_token, limit=12):
        """
        Получает посты из Instagram через Graph API с поддержкой пагинации
        
        Args:
            account_id: ID Instagram Business аккаунта
            access_token: Access Token для API
            limit: Количество постов для получения (0 = все доступные)
            
        Returns:
            list: Список постов
        """
        url = f"https://graph.instagram.com/{account_id}/media"
        
        params = {
            'fields': 'id,media_type,media_url,thumbnail_url,permalink,caption,timestamp,like_count,comments_count',
            'limit': min(limit, 100) if limit > 0 else 100,  # Instagram API максимум 100 за запрос
            'access_token': access_token,
        }
        
        all_posts = []
        
        try:
            while True:
                response = requests.get(url, params=params, timeout=30)
                response.raise_for_status()
                
                data = response.json()
                
                if 'error' in data:
                    error = data['error']
                    self.stdout.write(
                        self.style.ERROR(
                            f'Ошибка Instagram API: {error.get("message", "Unknown error")}\n'
                            f'Тип: {error.get("type", "Unknown")}\n'
                            f'Код: {error.get("code", "Unknown")}'
                        )
                    )
                    break
                
                if 'data' in data:
                    posts = data['data']
                    all_posts.extend(posts)
                    
                    # Если получили меньше постов, чем запросили, значит это последняя страница
                    if len(posts) < params['limit']:
                        break
                    
                    # Если достигли нужного лимита
                    if limit > 0 and len(all_posts) >= limit:
                        all_posts = all_posts[:limit]
                        break
                    
                    # Проверяем наличие следующей страницы
                    if 'paging' in data and 'next' in data['paging']:
                        url = data['paging']['next']
                        params = {}  # URL уже содержит все параметры
                    else:
                        break
                else:
                    self.stdout.write(
                        self.style.WARNING(f'Неожиданный формат ответа: {data}')
                    )
                    break
                
        except requests.exceptions.Timeout:
            self.stdout.write(
                self.style.ERROR('Таймаут при запросе к Instagram API')
            )
        except requests.exceptions.RequestException as e:
            self.stdout.write(
                self.style.ERROR(f'Ошибка при запросе к Instagram API: {str(e)}')
            )
        
        return all_posts
