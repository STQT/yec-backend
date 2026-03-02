# Generated manually

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0038_instagrampost_local_media'),
    ]

    operations = [
        migrations.AlterField(
            model_name='instagrampost',
            name='media_image',
            field=models.FileField(
                blank=True,
                help_text='Скачанное изображение или видео для локального использования',
                null=True,
                upload_to='instagram/media/%Y/%m/',
                verbose_name='Локальное медиа'
            ),
        ),
    ]
