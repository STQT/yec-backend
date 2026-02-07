"""
Management команда для создания сессии Instagram в Docker volume

Использование:
    docker compose -f docker-compose.production.yml run --rm django python manage.py create_instagram_session
    
    Или с указанием username:
    docker compose -f docker-compose.production.yml run --rm django python manage.py create_instagram_session --username YOUR_USERNAME
"""

import os
import instaloader
from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
import getpass


class Command(BaseCommand):
    help = 'Создает сессию Instagram и сохраняет её в Docker volume'

    def add_arguments(self, parser):
        parser.add_argument(
            '--username',
            type=str,
            help='Instagram username для создания сессии (по умолчанию из настроек)',
        )

    def handle(self, *args, **options):
        username = options.get('username') or getattr(settings, 'INSTAGRAM_LOGIN_USERNAME', None)
        
        if not username:
            username = input('Введите Instagram username: ').strip()
            if not username:
                raise CommandError('Username обязателен')
        
        session_dir = getattr(settings, 'INSTAGRAM_SESSION_DIR', '/app/.config/instaloader')
        os.makedirs(session_dir, exist_ok=True)
        sessions_dir = os.path.join(session_dir, 'sessions')
        os.makedirs(sessions_dir, exist_ok=True)
        
        self.stdout.write(f'Создаю сессию для @{username}...')
        self.stdout.write('Сессия будет сохранена в Docker volume и сохранится между перезапусками.')
        
        # Запрашиваем пароль
        password = getpass.getpass('Введите пароль Instagram: ')
        if not password:
            raise CommandError('Пароль обязателен')
        
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
            )
            
            # Устанавливаем рабочую директорию для instaloader (он сохранит сессию туда)
            original_dir = os.getcwd()
            try:
                os.chdir(sessions_dir)
                
                # Выполняем авторизацию
                loader.login(username, password)
                
                # Сохраняем сессию в volume (instaloader сохранит в текущей директории)
                loader.save_session_to_file(username)
                session_file = os.path.join(sessions_dir, username)
                
                self.stdout.write(
                    self.style.SUCCESS(
                        f'✓ Сессия успешно создана и сохранена в: {session_file}\n'
                        f'  Сессия будет доступна после перезапуска контейнера.'
                    )
                )
                
                self.stdout.write(
                    self.style.SUCCESS(
                        '\nТеперь вы можете использовать синхронизацию с авторизацией:\n'
                        f'  docker compose -f docker-compose.production.yml run --rm django \\\n'
                        f'    python manage.py sync_instagram_posts_opensource \\\n'
                        f'    --login-username {username}'
                    )
                )
                
            except instaloader.exceptions.BadCredentialsException:
                raise CommandError('Ошибка: Неверные учетные данные Instagram')
            except instaloader.exceptions.TwoFactorAuthRequiredException:
                raise CommandError(
                    'Ошибка: Требуется двухфакторная аутентификация.\n'
                    'Для аккаунтов с 2FA используйте временный код доступа или отключите 2FA.'
                )
            except Exception as e:
                raise CommandError(f'Ошибка при создании сессии: {str(e)}')
            finally:
                os.chdir(original_dir)
                
        except Exception as e:
            raise CommandError(f'Ошибка: {str(e)}')
