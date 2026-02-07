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
            except instaloader.exceptions.ConnectionException as e:
                error_msg = str(e)
                if "Checkpoint required" in error_msg or "challenge" in error_msg.lower():
                    # Извлекаем URL проверки из сообщения об ошибке
                    import re
                    challenge_url_match = re.search(r'https://www\.instagram\.com[^\s]+', error_msg)
                    challenge_url = challenge_url_match.group(0) if challenge_url_match else None
                    
                    raise CommandError(
                        'Ошибка: Instagram требует проверку безопасности (Checkpoint).\n\n'
                        'Решение:\n'
                        '1. Откройте ссылку проверки в браузере (желательно на том же устройстве/IP):\n'
                        f'   {challenge_url if challenge_url else "Ссылка в сообщении об ошибке"}\n'
                        '2. Пройдите проверку безопасности в браузере\n'
                        '3. Подождите 10-15 минут после прохождения проверки\n'
                        '4. Попробуйте создать сессию снова\n\n'
                        'Альтернативный способ:\n'
                        '1. Войдите в Instagram через браузер на том же IP-адресе\n'
                        '2. Используйте Instagram App на мобильном устройстве\n'
                        '3. Подождите несколько часов и попробуйте снова\n'
                        '4. Используйте другой аккаунт Instagram для авторизации'
                    )
                else:
                    raise CommandError(f'Ошибка подключения: {str(e)}')
            except Exception as e:
                error_msg = str(e)
                if "Checkpoint required" in error_msg or "challenge" in error_msg.lower():
                    import re
                    challenge_url_match = re.search(r'https://www\.instagram\.com[^\s]+', error_msg)
                    challenge_url = challenge_url_match.group(0) if challenge_url_match else None
                    
                    raise CommandError(
                        'Ошибка: Instagram требует проверку безопасности (Checkpoint).\n\n'
                        'Решение:\n'
                        '1. Откройте ссылку проверки в браузере:\n'
                        f'   {challenge_url if challenge_url else "Ссылка в сообщении об ошибке"}\n'
                        '2. Пройдите проверку безопасности\n'
                        '3. Подождите 10-15 минут и попробуйте снова\n\n'
                        'Или используйте другой аккаунт Instagram.'
                    )
                else:
                    raise CommandError(f'Ошибка при создании сессии: {str(e)}')
            finally:
                os.chdir(original_dir)
                
        except Exception as e:
            raise CommandError(f'Ошибка: {str(e)}')
