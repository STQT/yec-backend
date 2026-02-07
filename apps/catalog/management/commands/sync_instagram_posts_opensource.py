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
        parser.add_argument(
            '--login-username',
            type=str,
            help='Instagram username для авторизации (по умолчанию из настроек)',
        )
        parser.add_argument(
            '--login-password',
            type=str,
            help='Instagram password для авторизации (по умолчанию из настроек)',
        )

    def handle(self, *args, **options):
        limit = 0 if options.get('all') else options['limit']
        username = options.get('username') or getattr(settings, 'INSTAGRAM_USERNAME', 'yecgilam')
        delay = options.get('delay', 2.0)
        login_username = options.get('login_username') or getattr(settings, 'INSTAGRAM_LOGIN_USERNAME', None)
        login_password = options.get('login_password') or getattr(settings, 'INSTAGRAM_LOGIN_PASSWORD', None)
        session_dir = getattr(settings, 'INSTAGRAM_SESSION_DIR', '/app/.config/instaloader')
        
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
                quiet=True,  # Подавляем лишние сообщения об ошибках
            )
            
            # Устанавливаем директорию для сессий (из volume)
            import os
            os.makedirs(session_dir, exist_ok=True)
            sessions_dir = os.path.join(session_dir, 'sessions')
            os.makedirs(sessions_dir, exist_ok=True)
            
            # Устанавливаем директорию для instaloader (он сам управляет сессиями)
            # Instaloader будет искать сессии в стандартных местах, но мы можем указать кастомный путь
            
            # Устанавливаем задержку между запросами
            loader.request_timeout = 30
            loader.context._session.request_timeout = 30
            
            # Авторизация, если указаны учетные данные
            if login_username:
                if login_password:
                    # Авторизация по логину/паролю
                    try:
                        self.stdout.write(f'Выполняю авторизацию как @{login_username}...')
                        loader.login(login_username, login_password)
                        # Сохраняем сессию в volume
                        session_file = os.path.join(sessions_dir, login_username)
                        loader.save_session_to_file(session_file)
                        self.stdout.write(self.style.SUCCESS('Авторизация успешна, сессия сохранена'))
                    except instaloader.exceptions.BadCredentialsException:
                        self.stdout.write(
                            self.style.ERROR('Ошибка: Неверные учетные данные Instagram')
                        )
                        return
                    except instaloader.exceptions.TwoFactorAuthRequiredException:
                        self.stdout.write(
                            self.style.ERROR('Ошибка: Требуется двухфакторная аутентификация.')
                        )
                        return
                    except Exception as e:
                        self.stdout.write(
                            self.style.WARNING(f'Ошибка при авторизации: {str(e)}')
                        )
                        self.stdout.write('Продолжаю без авторизации...')
                else:
                    # Загрузка сессии из volume
                    try:
                        session_file = os.path.join(sessions_dir, login_username)
                        # Проверяем наличие файлов сессии
                        import glob
                        session_files = glob.glob(f"{session_file}-session-*")
                        
                        # Стандартное расположение instaloader в контейнере
                        standard_session_dir = os.path.expanduser('~/.config/instaloader')
                        os.makedirs(standard_session_dir, exist_ok=True)
                        standard_session_file = os.path.join(standard_session_dir, login_username)
                        
                        if os.path.exists(session_file) or session_files:
                            self.stdout.write(f'Загружаю сессию для @{login_username}...')
                            
                            # Копируем все файлы сессии в стандартное место instaloader
                            import shutil
                            import glob as glob_module
                            
                            # Копируем все файлы сессии (включая файлы с префиксами)
                            all_session_files = glob_module.glob(f"{sessions_dir}/{login_username}*")
                            
                            # Также копируем в место, где instaloader ищет по умолчанию
                            instaloader_tmp_dir = '/tmp/.instaloader-root'
                            os.makedirs(instaloader_tmp_dir, exist_ok=True)
                            
                            # Копируем файлы в оба места
                            for session_file_path in all_session_files:
                                if os.path.isfile(session_file_path):
                                    filename = os.path.basename(session_file_path)
                                    
                                    # Копируем в стандартное место
                                    dest_file = os.path.join(standard_session_dir, filename)
                                    shutil.copy2(session_file_path, dest_file)
                                    
                                    # Копируем в /tmp/.instaloader-root/
                                    dest_file_tmp = os.path.join(instaloader_tmp_dir, filename)
                                    shutil.copy2(session_file_path, dest_file_tmp)
                                    
                                    # Если файл без префикса session-, создаем копию с префиксом
                                    if filename == login_username:
                                        session_filename = f"session-{login_username}"
                                        dest_file_session = os.path.join(standard_session_dir, session_filename)
                                        dest_file_tmp_session = os.path.join(instaloader_tmp_dir, session_filename)
                                        shutil.copy2(session_file_path, dest_file_session)
                                        shutil.copy2(session_file_path, dest_file_tmp_session)
                                        self.stdout.write(f'  Скопирован файл: {filename} и создан {session_filename}')
                                    else:
                                        self.stdout.write(f'  Скопирован файл: {filename}')
                            
                            # Загружаем сессию из стандартного места
                            original_dir = os.getcwd()
                            try:
                                os.chdir(standard_session_dir)
                                loader.load_session_from_file(login_username)
                                self.stdout.write(self.style.SUCCESS('Сессия загружена успешно'))
                            finally:
                                os.chdir(original_dir)
                        else:
                            self.stdout.write(
                                self.style.WARNING(
                                    f'Файл сессии не найден для @{login_username}.\n'
                                    f'Ожидаемый путь: {session_file}\n'
                                    f'Создайте сессию командой: python manage.py create_instagram_session --username {login_username}\n'
                                    'Продолжаю без авторизации...'
                                )
                            )
                    except Exception as e:
                        self.stdout.write(
                            self.style.WARNING(f'Ошибка при загрузке сессии: {str(e)}')
                        )
                        import traceback
                        self.stdout.write(traceback.format_exc())
                        self.stdout.write('Продолжаю без авторизации...')
            
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
