"""
Management команда для загрузки постов Instagram из JSON в базу и скачивания медиа для локального использования.

Использование:
    # Загрузка из instagram_posts.json (путь по умолчанию)
    python manage.py load_instagram_from_json

    # Загрузка из указанного файла
    python manage.py load_instagram_from_json path/to/posts.json

    # Загрузка + скачивание медиафайлов для локального использования
    python manage.py load_instagram_from_json instagram_posts.json --download

    # Обновление существующих постов
    python manage.py load_instagram_from_json --update

    # Dry-run (только показать что будет сделано)
    python manage.py load_instagram_from_json --dry-run

Формат JSON (см. instagram_posts.json):
{
  "username": "yecgilam",
  "posts": [
    {
      "instagram_id": "ABC123",
      "post_type": "IMAGE",
      "caption": "...",
      "permalink": "https://...",
      "thumbnail_url": "https://...",
      "media_url": "https://...",
      "like_count": 0,
      "comments_count": 0,
      "timestamp": "2026-03-02T08:38:23+00:00"
    }
  ]
}
"""

import json
import mimetypes
from datetime import datetime
from pathlib import Path
from urllib.request import Request, urlopen
from urllib.error import URLError

from django.conf import settings
from django.core.files.base import ContentFile
from django.core.management.base import BaseCommand, CommandError
from django.utils import timezone

from apps.catalog.models import InstagramPost


class Command(BaseCommand):
    help = 'Загружает посты Instagram из JSON в базу и опционально скачивает медиа для локального использования'

    def add_arguments(self, parser):
        parser.add_argument(
            'json_file',
            nargs='?',
            type=str,
            default='instagram_posts.json',
            help='Путь к JSON файлу (по умолчанию: instagram_posts.json)',
        )
        parser.add_argument(
            '--download',
            action='store_true',
            help='Скачать медиафайлы (thumbnail, media) для локального использования',
        )
        parser.add_argument(
            '--update',
            action='store_true',
            help='Обновлять существующие посты (по умолчанию только создавать новые)',
        )
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Показать что будет сделано без сохранения в базу',
        )

    def handle(self, *args, **options):
        json_file = options['json_file']
        download_files = options['download']
        update_existing = options['update']
        dry_run = options['dry_run']

        # Ищем файл: сначала указанный путь, затем от корня проекта
        if not Path(json_file).is_absolute():
            project_root = Path(settings.BASE_DIR)
            candidates = [
                project_root / json_file,
                project_root / 'instagram_posts.json',
            ]
            for path in candidates:
                if path.exists():
                    json_file = str(path)
                    break
            else:
                raise CommandError(
                    f'Файл не найден: {json_file}\n'
                    f'Проверенные пути: {[str(p) for p in candidates]}'
                )

        if dry_run:
            self.stdout.write(
                self.style.WARNING('🔍 Режим DRY-RUN: данные не будут сохранены в базу')
            )

        # Читаем JSON
        try:
            with open(json_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
        except FileNotFoundError:
            raise CommandError(f'Файл не найден: {json_file}')
        except json.JSONDecodeError as e:
            raise CommandError(f'Ошибка чтения JSON: {e}')

        if 'posts' not in data:
            raise CommandError('Неверный формат JSON: отсутствует ключ "posts"')

        posts_data = data['posts']
        username = data.get('username', 'unknown')
        collected_at = data.get('collected_at', 'unknown')
        total_posts = len(posts_data)

        self.stdout.write(
            self.style.SUCCESS(
                f'📄 Файл: {json_file}\n'
                f'👤 Профиль: @{username}\n'
                f'🕐 Собрано: {collected_at}\n'
                f'📊 Всего постов: {total_posts}\n'
                f'📥 Скачивание медиа: {"да" if download_files else "нет"}'
            )
        )

        if not posts_data:
            self.stdout.write(self.style.WARNING('⚠️  Нет постов для импорта'))
            return

        created_count = 0
        updated_count = 0
        skipped_count = 0
        error_count = 0
        downloaded_count = 0

        for i, post_data in enumerate(posts_data, 1):
            try:
                instagram_id = post_data.get('instagram_id')
                if not instagram_id:
                    self.stdout.write(
                        self.style.WARNING(f'  ⚠️  Пост {i}: пропущен (нет instagram_id)')
                    )
                    skipped_count += 1
                    continue

                exists = InstagramPost.objects.filter(instagram_id=instagram_id).exists()
                if exists and not update_existing:
                    self.stdout.write(
                        self.style.WARNING(f'  ⊗ Пост {i}: {instagram_id} уже существует (пропущен)')
                    )
                    skipped_count += 1
                    continue

                # Парсим timestamp
                timestamp_str = post_data.get('timestamp')
                if timestamp_str:
                    try:
                        if 'T' in timestamp_str:
                            timestamp = datetime.fromisoformat(
                                timestamp_str.replace('Z', '+00:00')
                            )
                        else:
                            timestamp = datetime.strptime(
                                timestamp_str, '%Y-%m-%d %H:%M:%S'
                            )
                            timestamp = timezone.make_aware(timestamp)
                    except (ValueError, TypeError) as e:
                        self.stdout.write(
                            self.style.WARNING(f'  ⚠️  Пост {i}: ошибка timestamp: {e}')
                        )
                        timestamp = timezone.now()
                else:
                    timestamp = timezone.now()

                defaults = {
                    'post_type': post_data.get('post_type', 'IMAGE'),
                    'caption': (
                        post_data.get('caption', '')[:5000]
                        if post_data.get('caption')
                        else None
                    ),
                    'permalink': post_data.get('permalink', ''),
                    'thumbnail_url': post_data.get('thumbnail_url') or '',
                    'media_url': post_data.get('media_url') or '',
                    'like_count': post_data.get('like_count', 0),
                    'comments_count': post_data.get('comments_count', 0),
                    'timestamp': timestamp,
                }

                if dry_run:
                    action = 'обновлен' if exists else 'создан'
                    self.stdout.write(
                        f'  [DRY-RUN] Пост {i}: {instagram_id} будет {action} '
                        f'({defaults["post_type"]}, {defaults["like_count"]} ❤️)'
                    )
                    if exists:
                        updated_count += 1
                    else:
                        created_count += 1
                else:
                    post, created = InstagramPost.objects.update_or_create(
                        instagram_id=instagram_id,
                        defaults=defaults,
                    )

                    if created:
                        created_count += 1
                        self.stdout.write(
                            self.style.SUCCESS(
                                f'  ✓ Пост {i}: {instagram_id} создан '
                                f'({post.post_type}, {post.like_count} ❤️)'
                            )
                        )
                    else:
                        updated_count += 1
                        self.stdout.write(
                            f'  ↻ Пост {i}: {instagram_id} обновлен '
                            f'({post.post_type}, {post.like_count} ❤️)'
                        )

                    # Скачиваем медиа для локального использования
                    if download_files and post:
                        downloaded = self._download_media(post)
                        if downloaded:
                            downloaded_count += downloaded

            except Exception as e:
                error_count += 1
                self.stdout.write(
                    self.style.ERROR(f'  ✗ Пост {i}: ошибка - {str(e)}')
                )
                continue

        # Итог
        self.stdout.write('\n' + '=' * 60)
        if dry_run:
            self.stdout.write(
                self.style.WARNING(
                    '🔍 Результаты DRY-RUN (данные не сохранены):\n'
                    f'  Будет создано: {created_count}\n'
                    f'  Будет обновлено: {updated_count}\n'
                    f'  Будет пропущено: {skipped_count}\n'
                    f'  Ошибок: {error_count}\n'
                    f'  Всего: {total_posts}'
                )
            )
        else:
            self.stdout.write(
                self.style.SUCCESS(
                    '✅ Загрузка завершена:\n'
                    f'  Создано: {created_count}\n'
                    f'  Обновлено: {updated_count}\n'
                    f'  Пропущено: {skipped_count}\n'
                    f'  Скачано медиа: {downloaded_count}\n'
                    f'  Ошибок: {error_count}\n'
                    f'  Всего: {total_posts}'
                )
            )

        if not dry_run and (created_count > 0 or updated_count > 0):
            self.stdout.write(
                '\n📊 Посты доступны:\n'
                '  - Админка: /admin/catalog/instagrampost/\n'
                '  - API: /api/instagram-posts/'
            )

    def _download_media(self, post: InstagramPost) -> int:
        """Скачивает thumbnail и media, сохраняет в локальные поля. Возвращает кол-во скачанных."""
        downloaded = 0

        # Скачиваем thumbnail
        if post.thumbnail_url and not post.thumbnail_image:
            if self._download_and_save(post, 'thumbnail_url', 'thumbnail_image'):
                downloaded += 1

        # Скачиваем media (если отличается от thumbnail)
        if post.media_url and not post.media_image:
            if post.media_url != post.thumbnail_url:
                if self._download_and_save(post, 'media_url', 'media_image'):
                    downloaded += 1
            else:
                # media_url == thumbnail_url — копируем thumbnail в media
                if post.thumbnail_image:
                    post.media_image.save(
                        f"{post.instagram_id}_media.jpg",
                        ContentFile(post.thumbnail_image.read()),
                        save=True,
                    )
                    downloaded += 1
                elif self._download_and_save(post, 'media_url', 'media_image'):
                    downloaded += 1

        return downloaded

    def _download_and_save(
        self,
        post: InstagramPost,
        url_field: str,
        file_field: str,
    ) -> bool:
        """Скачивает URL и сохраняет в поле модели. Возвращает True при успехе."""
        url = getattr(post, url_field)
        if not url:
            return False

        try:
            req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            with urlopen(req, timeout=30) as response:
                content = response.read()
                content_type = response.headers.get('Content-Type', '')
        except (URLError, OSError) as e:
            self.stdout.write(
                self.style.WARNING(f'    ⚠️  Ошибка загрузки {url[:50]}...: {e}')
            )
            return False

        # Определяем расширение (media_image — FileField, поддерживает видео)
        ext = '.jpg'
        if 'image/' in content_type:
            ext = mimetypes.guess_extension(
                content_type.split(';')[0].strip() or 'image/jpeg'
            ) or '.jpg'
        elif 'video/' in content_type:
            if content[:4] == b'\xff\xd8\xff':
                ext = '.jpg'  # JPEG под видом video
            elif file_field == 'media_image':
                ext = mimetypes.guess_extension(
                    content_type.split(';')[0].strip() or 'video/mp4'
                ) or '.mp4'
            else:
                return False  # thumbnail_image — только изображения

        filename = f"{post.instagram_id}_{file_field}{ext}"

        try:
            getattr(post, file_field).save(
                filename,
                ContentFile(content),
                save=True,
            )
            self.stdout.write(f'    📥 Скачано: {file_field} -> {filename}')
            return True
        except Exception as e:
            self.stdout.write(
                self.style.WARNING(f'    ⚠️  Ошибка сохранения {file_field}: {e}')
            )
            return False
