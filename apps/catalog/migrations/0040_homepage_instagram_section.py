# Generated manually: add Instagram section multilingual fields to HomePage

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0039_alter_instagrampost_media_to_filefield'),
    ]

    operations = [
        migrations.AddField(
            model_name='homepage',
            name='instagram_section_title',
            field=models.CharField(
                blank=True,
                max_length=200,
                null=True,
                verbose_name='Заголовок секции Instagram'
            ),
        ),
        migrations.AddField(
            model_name='homepage',
            name='instagram_section_title_uz',
            field=models.CharField(
                blank=True,
                max_length=200,
                null=True,
                verbose_name='Заголовок секции Instagram'
            ),
        ),
        migrations.AddField(
            model_name='homepage',
            name='instagram_section_title_ru',
            field=models.CharField(
                blank=True,
                max_length=200,
                null=True,
                verbose_name='Заголовок секции Instagram'
            ),
        ),
        migrations.AddField(
            model_name='homepage',
            name='instagram_section_title_en',
            field=models.CharField(
                blank=True,
                max_length=200,
                null=True,
                verbose_name='Заголовок секции Instagram'
            ),
        ),
        migrations.AddField(
            model_name='homepage',
            name='instagram_section_text',
            field=models.TextField(
                blank=True,
                null=True,
                verbose_name='Текст секции Instagram'
            ),
        ),
        migrations.AddField(
            model_name='homepage',
            name='instagram_section_text_uz',
            field=models.TextField(
                blank=True,
                null=True,
                verbose_name='Текст секции Instagram'
            ),
        ),
        migrations.AddField(
            model_name='homepage',
            name='instagram_section_text_ru',
            field=models.TextField(
                blank=True,
                null=True,
                verbose_name='Текст секции Instagram'
            ),
        ),
        migrations.AddField(
            model_name='homepage',
            name='instagram_section_text_en',
            field=models.TextField(
                blank=True,
                null=True,
                verbose_name='Текст секции Instagram'
            ),
        ),
    ]
