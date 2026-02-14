"""
Management команда для импорта постов Instagram из JSON файла

Использование:
    # Импорт постов из JSON (только новые посты)
    python manage.py import_instagram_from_json instagram_posts.json

    # Импорт с обновлением существующих постов
    python manage.py import_instagram_from_json instagram_posts.json --update

    # Dry-run (только показать что будет импортировано)
    python manage.py import_instagram_from_json instagram_posts.json --dry-run

Формат JSON файла:
{
  "username": "yecgilam",
  "collected_at": "2024-01-15 10:30:00 UTC",
  "total_posts": 12,
  "posts": [
    {
      "instagram_id": "ABC123",
      "post_type": "IMAGE",
      "caption": "Caption text",
      "permalink": "https://www.instagram.com/p/ABC123/",
      "thumbnail_url": "https://...",
      "media_url": "https://...",
      "like_count": 100,
      "comments_count": 5,
      "timestamp": "2024-01-15T10:30:00+00:00"
    }
  ]
}
"""

import json
from django.core.management.base import BaseCommand, CommandError
from django.utils import timezone
from apps.catalog.models import InstagramPost
from datetime import datetime


class Command(BaseCommand):
    help = 'Импортирует посты Instagram из JSON файла'

    def add_arguments(self, parser):
        parser.add_argument(
            'json_file',
            type=str,
            help='Путь к JSON файлу с постами'
        )
        parser.add_argument(
            '--update',
            action='store_true',
            help='Обновлять существующие посты (по умолчанию только создавать новые)'
        )
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Показать что будет импортировано без сохранения в базу'
        )

    def handle(self, *args, **options):
        json_file = options['json_file']
        update_existing = options['update']
        dry_run = options['dry_run']

        if dry_run:
            self.stdout.write(
                self.style.WARNING('🔍 Режим DRY-RUN: данные не будут сохранены в базу')
            )

        # Читаем JSON файл
        try:
            with open(json_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
        except FileNotFoundError:
            raise CommandError(f'Файл не найден: {json_file}')
        except json.JSONDecodeError as e:
            raise CommandError(f'Ошибка чтения JSON: {e}')

        # Проверяем структуру данных
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
                f'📊 Всего постов: {total_posts}'
            )
        )

        if not posts_data:
            self.stdout.write(self.style.WARNING('⚠️  Нет постов для импорта'))
            return

        # Обрабатываем посты
        created_count = 0
        updated_count = 0
        skipped_count = 0
        error_count = 0

        for i, post_data in enumerate(posts_data, 1):
            try:
                instagram_id = post_data.get('instagram_id')
                if not instagram_id:
                    self.stdout.write(
                        self.style.WARNING(f'  ⚠️  Пост {i}: пропущен (нет instagram_id)')
                    )
                    skipped_count += 1
                    continue

                # Проверяем существование поста
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
                        # Пробуем разные форматы
                        if 'T' in timestamp_str:
                            # ISO формат
                            timestamp = datetime.fromisoformat(timestamp_str.replace('Z', '+00:00'))
                        else:
                            # Другие форматы
                            timestamp = datetime.strptime(timestamp_str, '%Y-%m-%d %H:%M:%S')
                            timestamp = timezone.make_aware(timestamp)
                    except (ValueError, TypeError) as e:
                        self.stdout.write(
                            self.style.WARNING(f'  ⚠️  Пост {i}: ошибка парсинга timestamp: {e}')
                        )
                        timestamp = timezone.now()
                else:
                    timestamp = timezone.now()

                # Подготавливаем данные
                defaults = {
                    'post_type': post_data.get('post_type', 'IMAGE'),
                    'caption': post_data.get('caption', '')[:5000] if post_data.get('caption') else None,
                    'permalink': post_data.get('permalink', ''),
                    'thumbnail_url': post_data.get('thumbnail_url', ''),
                    'media_url': post_data.get('media_url', ''),
                    'like_count': post_data.get('like_count', 0),
                    'comments_count': post_data.get('comments_count', 0),
                    'timestamp': timestamp,
                }

                if dry_run:
                    # Dry-run: только показываем что будет сделано
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
                    # Создаем или обновляем пост
                    post, created = InstagramPost.objects.update_or_create(
                        instagram_id=instagram_id,
                        defaults=defaults
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

            except Exception as e:
                error_count += 1
                self.stdout.write(
                    self.style.ERROR(f'  ✗ Пост {i}: ошибка - {str(e)}')
                )
                continue

        # Итоговая статистика
        self.stdout.write('\n' + '=' * 60)
        if dry_run:
            self.stdout.write(
                self.style.WARNING(
                    '🔍 Результаты DRY-RUN (данные не сохранены):\n'
                    f'  Будет создано: {created_count}\n'
                    f'  Будет обновлено: {updated_count}\n'
                    f'  Будет пропущено: {skipped_count}\n'
                    f'  Ошибок: {error_count}\n'
                    f'  Всего обработано: {total_posts}'
                )
            )
        else:
            self.stdout.write(
                self.style.SUCCESS(
                    '✅ Импорт завершен:\n'
                    f'  Создано: {created_count}\n'
                    f'  Обновлено: {updated_count}\n'
                    f'  Пропущено: {skipped_count}\n'
                    f'  Ошибок: {error_count}\n'
                    f'  Всего обработано: {total_posts}'
                )
            )

        if not dry_run and (created_count > 0 or updated_count > 0):
            self.stdout.write(
                '\n📊 Посты доступны:\n'
                '  - Админка: /admin/catalog/instagrampost/\n'
                '  - API: /api/instagram-posts/'
            )
