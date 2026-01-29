# Generated manually: simplify News model - remove blocks, add content field

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0020_merge_0018_merge_20260129_2342_0019_rework_aboutpage'),
    ]

    operations = [
        # Удаляем модели NewsImage и NewsContentBlock
        migrations.DeleteModel(
            name='NewsImage',
        ),
        migrations.DeleteModel(
            name='NewsContentBlock',
        ),
        # Добавляем поле content в News
        migrations.AddField(
            model_name='news',
            name='content',
            field=models.TextField(
                blank=True,
                null=True,
                verbose_name='Содержание',
                help_text='Полное содержание новости. Поддерживает HTML (CKEditor)'
            ),
        ),
        # Добавляем мультиязычные поля для content (будут созданы modeltranslation автоматически)
        migrations.AddField(
            model_name='news',
            name='content_uz',
            field=models.TextField(
                blank=True,
                null=True,
                verbose_name='Содержание'
            ),
        ),
        migrations.AddField(
            model_name='news',
            name='content_ru',
            field=models.TextField(
                blank=True,
                null=True,
                verbose_name='Содержание'
            ),
        ),
        migrations.AddField(
            model_name='news',
            name='content_en',
            field=models.TextField(
                blank=True,
                null=True,
                verbose_name='Содержание'
            ),
        ),
    ]
