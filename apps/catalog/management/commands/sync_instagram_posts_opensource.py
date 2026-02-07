"""
Management команда для синхронизации постов из Instagram через open source решение

Использование:
    python manage.py sync_instagram_posts_opensource

Этот метод использует библиотеку instaloader для получения постов из публичного профиля Instagram.
Не требует Instagram Business аккаунт или Facebook App.

Преимущества:
- Не требует Business аккаунт
- Не требует Facebook App
- Работает с публичными профилями
- Не нарушает ToS (использует публичные данные)

Ограничения:
- Работает только с публичными профилями
- Может быть медленнее, чем официальный API
- Может быть заблокирован при частых запросах (рекомендуется использовать задержки)
"""

import instaloader
from datetime import timezone
from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
from django.utils import timezone as django_timezone
from apps.catalog.models import InstagramPost


class Command(BaseCommand):
    help = 'Синхронизирует посты из Instagram через instaloader (open source решение)'

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
        parser.add_argument(
            '--delay',
            type=float,
            default=2.0,
            help='Задержка между запросами в секундах (по умолчанию: 2.0)',
        )

    def handle(self, *args, **options):
        limit = 0 if options.get('all') else options['limit']
        username = options.get('username') or getattr(settings, 'INSTAGRAM_USERNAME', 'yecgilam')
        delay = options.get('delay', 2.0)
        
        self.stdout.write(
            self.style.SUCCESS(f'Начинаю синхронизацию постов из профиля @{username}...')
        )
        
        try:
            # Создаем экземпляр Instaloader
            loader = instaloader.Instaloader(
                download_videos=False,
                download_video_thumbnails=False,
                download_geotags=False,
                download_comments=False,
                save_metadata=False,
                compress_json=False,
                post_metadata_txt_pattern='',
                max_connection_attempts=3,
            )
            
            # Устанавливаем задержку между запросами
            loader.request_timeout = 30
            loader.context._session.request_timeout = 30
            
            # Получаем профиль
            self.stdout.write(f'Получаю профиль @{username}...')
            profile = instaloader.Profile.from_username(loader.context, username)
            
            if not profile.is_private:
                self.stdout.write(
                    self.style.SUCCESS(f'Профиль @{username} найден (публичный)')
                )
            else:
                self.stdout.write(
                    self.style.WARNING(
                        f'Профиль @{username} является приватным. '
                        'Для приватных профилей требуется авторизация.'
                    )
                )
                return
            
            # Получаем посты
            self.stdout.write('Получаю посты...')
            posts = self.fetch_instagram_posts(profile, limit, delay)
            
            if not posts:
                self.stdout.write(
                    self.style.WARNING('Не удалось получить посты из Instagram')
                )
                return
            
            # Сохраняем посты в базу данных
            created_count = 0
            updated_count = 0
            
            for post in posts:
                try:
                    instagram_id = str(post.shortcode)
                    if not instagram_id:
                        continue
                    
                    # Определяем тип поста
                    if post.is_video:
                        post_type = 'VIDEO'
                    elif post.typename == 'GraphSidecar':
                        post_type = 'CAROUSEL_ALBUM'
                    else:
                        post_type = 'IMAGE'
                    
                    # Получаем URL медиа
                    if post.is_video:
                        media_url = post.video_url if hasattr(post, 'video_url') else None
                        thumbnail_url = post.url if hasattr(post, 'url') else None
                    else:
                        media_url = post.url if hasattr(post, 'url') else None
                        thumbnail_url = post.url if hasattr(post, 'url') else None
                    
                    # Для каруселей берем первое изображение
                    if post_type == 'CAROUSEL_ALBUM' and hasattr(post, 'get_sidecar_nodes'):
                        try:
                            sidecar_nodes = list(post.get_sidecar_nodes())
                            if sidecar_nodes:
                                first_node = sidecar_nodes[0]
                                media_url = first_node.display_url if hasattr(first_node, 'display_url') else media_url
                                thumbnail_url = first_node.display_url if hasattr(first_node, 'display_url') else thumbnail_url
                        except Exception:
                            pass  # Если не удалось получить sidecar, используем основной URL
                    
                    # Получаем caption
                    caption = post.caption if post.caption else ''
                    
                    # Получаем permalink
                    permalink = f"https://www.instagram.com/p/{post.shortcode}/"
                    
                    # Получаем метрики
                    like_count = post.likes
                    comments_count = post.comments
                    
                    # Получаем timestamp
                    # post.date_utc уже возвращает datetime в UTC, но может не иметь tzinfo
                    timestamp = post.date_utc
                    if timestamp.tzinfo is None:
                        timestamp = timestamp.replace(tzinfo=timezone.utc)
                    
                    # Создаем или обновляем пост
                    post_obj, created = InstagramPost.objects.update_or_create(
                        instagram_id=instagram_id,
                        defaults={
                            'post_type': post_type,
                            'caption': caption[:5000] if caption else None,
                            'permalink': permalink,
                            'thumbnail_url': thumbnail_url,
                            'media_url': media_url,
                            'like_count': like_count,
                            'comments_count': comments_count,
                            'timestamp': timestamp,
                        }
                    )
                    
                    if created:
                        created_count += 1
                    else:
                        updated_count += 1
                        
                except Exception as e:
                    self.stdout.write(
                        self.style.WARNING(f'Ошибка при обработке поста: {str(e)}')
                    )
                    continue
            
            self.stdout.write(
                self.style.SUCCESS(
                    f'Успешно синхронизировано постов:\n'
                    f'  Создано: {created_count}\n'
                    f'  Обновлено: {updated_count}\n'
                    f'  Всего обработано: {len(posts)}'
                )
            )
            
        except instaloader.exceptions.ProfileNotExistsException:
            raise CommandError(f'Профиль @{username} не найден')
        except instaloader.exceptions.ConnectionException as e:
            raise CommandError(f'Ошибка подключения к Instagram: {str(e)}')
        except instaloader.exceptions.LoginRequiredException:
            raise CommandError(
                'Требуется авторизация. Для приватных профилей необходимо войти в аккаунт.'
            )
        except Exception as e:
            raise CommandError(f'Ошибка при синхронизации: {str(e)}')

    def fetch_instagram_posts(self, profile, limit=12, delay=2.0):
        """
        Получает посты из Instagram через instaloader
        
        Args:
            profile: Instaloader Profile объект
            limit: Количество постов для получения (0 = все доступные)
            delay: Задержка между запросами в секундах
            
        Returns:
            list: Список постов
        """
        all_posts = []
        
        try:
            # Получаем посты из профиля
            posts_iterator = profile.get_posts()
            
            count = 0
            for post in posts_iterator:
                all_posts.append(post)
                count += 1
                
                # Если достигли лимита
                if limit > 0 and count >= limit:
                    break
                
                # Небольшая задержка между запросами
                if delay > 0:
                    import time
                    time.sleep(delay)
                    
        except Exception as e:
            self.stdout.write(
                self.style.WARNING(f'Ошибка при получении постов: {str(e)}')
            )
        
        return all_posts
