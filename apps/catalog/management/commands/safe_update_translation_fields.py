from django.core.management.base import BaseCommand
from django.db import connection
from modeltranslation.management.commands.update_translation_fields import Command as UpdateTranslationFieldsCommand


class Command(BaseCommand):
    help = 'Безопасно обновляет поля перевода, пропуская модели с несуществующими таблицами'

    def handle(self, *args, **options):
        # Список моделей, которые могут не существовать
        models_to_skip = [
            'catalog_productionstep',
            'catalog_companyhistory',
            'catalog_productioncapacity',
        ]
        
        # Проверяем существование таблиц
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT table_name 
                FROM information_schema.tables 
                WHERE table_schema = 'public' 
                AND table_name LIKE 'catalog_%'
            """)
            existing_tables = {row[0] for row in cursor.fetchall()}
        
        # Пропускаем модели с несуществующими таблицами
        missing_tables = [t for t in models_to_skip if t not in existing_tables]
        
        if missing_tables:
            self.stdout.write(
                self.style.WARNING(
                    f'Пропускаем модели с несуществующими таблицами: {", ".join(missing_tables)}\n'
                    'Примените миграции перед запуском этой команды.'
                )
            )
        
        # Запускаем стандартную команду
        try:
            update_cmd = UpdateTranslationFieldsCommand()
            update_cmd.handle(*args, **options)
        except Exception as e:
            if 'does not exist' in str(e):
                self.stdout.write(
                    self.style.ERROR(
                        f'Ошибка: {e}\n'
                        'Некоторые таблицы не существуют. Примените миграции сначала.'
                    )
                )
            else:
                raise
