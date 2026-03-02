# Generated manually

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0037_dealer_request_message_optional'),
    ]

    operations = [
        migrations.AddField(
            model_name='instagrampost',
            name='thumbnail_image',
            field=models.ImageField(
                blank=True,
                help_text='Скачанное изображение миниатюры для локального использования',
                null=True,
                upload_to='instagram/thumbnails/%Y/%m/',
                verbose_name='Локальная миниатюра'
            ),
        ),
        migrations.AddField(
            model_name='instagrampost',
            name='media_image',
            field=models.ImageField(
                blank=True,
                help_text='Скачанное изображение/превью для локального использования',
                null=True,
                upload_to='instagram/media/%Y/%m/',
                verbose_name='Локальное медиа'
            ),
        ),
    ]
