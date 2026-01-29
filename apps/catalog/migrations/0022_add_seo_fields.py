# Generated manually: add SEO fields to HomePage, AboutPage, ContactPage

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0021_simplify_news_content'),
    ]

    operations = [
        # ========== HOMEPAGE SEO FIELDS ==========
        migrations.AddField(
            model_name='homepage',
            name='meta_title',
            field=models.CharField(
                blank=True,
                null=True,
                max_length=70,
                verbose_name='Meta Title',
                help_text='Заголовок страницы для поисковых систем (рекомендуется до 60 символов)'
            ),
        ),
        migrations.AddField(
            model_name='homepage',
            name='meta_description',
            field=models.TextField(
                blank=True,
                null=True,
                max_length=160,
                verbose_name='Meta Description',
                help_text='Описание страницы для поисковых систем (рекомендуется до 160 символов)'
            ),
        ),
        migrations.AddField(
            model_name='homepage',
            name='meta_keywords',
            field=models.CharField(
                blank=True,
                null=True,
                max_length=255,
                verbose_name='Meta Keywords',
                help_text='Ключевые слова через запятую'
            ),
        ),
        migrations.AddField(
            model_name='homepage',
            name='og_title',
            field=models.CharField(
                blank=True,
                null=True,
                max_length=100,
                verbose_name='OG Title',
                help_text='Заголовок для социальных сетей (Facebook, Twitter и т.д.)'
            ),
        ),
        migrations.AddField(
            model_name='homepage',
            name='og_description',
            field=models.TextField(
                blank=True,
                null=True,
                max_length=200,
                verbose_name='OG Description',
                help_text='Описание для социальных сетей'
            ),
        ),
        migrations.AddField(
            model_name='homepage',
            name='og_image',
            field=models.ImageField(
                blank=True,
                null=True,
                upload_to='photos/seo/%Y/%m/',
                verbose_name='OG Image',
                help_text='Изображение для социальных сетей (рекомендуется 1200x630px)'
            ),
        ),
        migrations.AddField(
            model_name='homepage',
            name='canonical_url',
            field=models.URLField(
                blank=True,
                null=True,
                max_length=500,
                verbose_name='Canonical URL',
                help_text='Канонический URL страницы (опционально)'
            ),
        ),
        # Мультиязычные поля для HomePage (будут созданы modeltranslation автоматически)
        migrations.AddField(
            model_name='homepage',
            name='meta_title_uz',
            field=models.CharField(blank=True, null=True, max_length=70, verbose_name='Meta Title'),
        ),
        migrations.AddField(
            model_name='homepage',
            name='meta_title_ru',
            field=models.CharField(blank=True, null=True, max_length=70, verbose_name='Meta Title'),
        ),
        migrations.AddField(
            model_name='homepage',
            name='meta_title_en',
            field=models.CharField(blank=True, null=True, max_length=70, verbose_name='Meta Title'),
        ),
        migrations.AddField(
            model_name='homepage',
            name='meta_description_uz',
            field=models.TextField(blank=True, null=True, max_length=160, verbose_name='Meta Description'),
        ),
        migrations.AddField(
            model_name='homepage',
            name='meta_description_ru',
            field=models.TextField(blank=True, null=True, max_length=160, verbose_name='Meta Description'),
        ),
        migrations.AddField(
            model_name='homepage',
            name='meta_description_en',
            field=models.TextField(blank=True, null=True, max_length=160, verbose_name='Meta Description'),
        ),
        migrations.AddField(
            model_name='homepage',
            name='meta_keywords_uz',
            field=models.CharField(blank=True, null=True, max_length=255, verbose_name='Meta Keywords'),
        ),
        migrations.AddField(
            model_name='homepage',
            name='meta_keywords_ru',
            field=models.CharField(blank=True, null=True, max_length=255, verbose_name='Meta Keywords'),
        ),
        migrations.AddField(
            model_name='homepage',
            name='meta_keywords_en',
            field=models.CharField(blank=True, null=True, max_length=255, verbose_name='Meta Keywords'),
        ),
        migrations.AddField(
            model_name='homepage',
            name='og_title_uz',
            field=models.CharField(blank=True, null=True, max_length=100, verbose_name='OG Title'),
        ),
        migrations.AddField(
            model_name='homepage',
            name='og_title_ru',
            field=models.CharField(blank=True, null=True, max_length=100, verbose_name='OG Title'),
        ),
        migrations.AddField(
            model_name='homepage',
            name='og_title_en',
            field=models.CharField(blank=True, null=True, max_length=100, verbose_name='OG Title'),
        ),
        migrations.AddField(
            model_name='homepage',
            name='og_description_uz',
            field=models.TextField(blank=True, null=True, max_length=200, verbose_name='OG Description'),
        ),
        migrations.AddField(
            model_name='homepage',
            name='og_description_ru',
            field=models.TextField(blank=True, null=True, max_length=200, verbose_name='OG Description'),
        ),
        migrations.AddField(
            model_name='homepage',
            name='og_description_en',
            field=models.TextField(blank=True, null=True, max_length=200, verbose_name='OG Description'),
        ),
        migrations.AddField(
            model_name='homepage',
            name='canonical_url_uz',
            field=models.URLField(blank=True, null=True, max_length=500, verbose_name='Canonical URL'),
        ),
        migrations.AddField(
            model_name='homepage',
            name='canonical_url_ru',
            field=models.URLField(blank=True, null=True, max_length=500, verbose_name='Canonical URL'),
        ),
        migrations.AddField(
            model_name='homepage',
            name='canonical_url_en',
            field=models.URLField(blank=True, null=True, max_length=500, verbose_name='Canonical URL'),
        ),
        
        # ========== ABOUTPAGE SEO FIELDS ==========
        migrations.AddField(
            model_name='aboutpage',
            name='meta_title',
            field=models.CharField(
                blank=True,
                null=True,
                max_length=70,
                verbose_name='Meta Title',
                help_text='Заголовок страницы для поисковых систем (рекомендуется до 60 символов)'
            ),
        ),
        migrations.AddField(
            model_name='aboutpage',
            name='meta_description',
            field=models.TextField(
                blank=True,
                null=True,
                max_length=160,
                verbose_name='Meta Description',
                help_text='Описание страницы для поисковых систем (рекомендуется до 160 символов)'
            ),
        ),
        migrations.AddField(
            model_name='aboutpage',
            name='meta_keywords',
            field=models.CharField(
                blank=True,
                null=True,
                max_length=255,
                verbose_name='Meta Keywords',
                help_text='Ключевые слова через запятую'
            ),
        ),
        migrations.AddField(
            model_name='aboutpage',
            name='og_title',
            field=models.CharField(
                blank=True,
                null=True,
                max_length=100,
                verbose_name='OG Title',
                help_text='Заголовок для социальных сетей (Facebook, Twitter и т.д.)'
            ),
        ),
        migrations.AddField(
            model_name='aboutpage',
            name='og_description',
            field=models.TextField(
                blank=True,
                null=True,
                max_length=200,
                verbose_name='OG Description',
                help_text='Описание для социальных сетей'
            ),
        ),
        migrations.AddField(
            model_name='aboutpage',
            name='og_image',
            field=models.ImageField(
                blank=True,
                null=True,
                upload_to='photos/seo/%Y/%m/',
                verbose_name='OG Image',
                help_text='Изображение для социальных сетей (рекомендуется 1200x630px)'
            ),
        ),
        migrations.AddField(
            model_name='aboutpage',
            name='canonical_url',
            field=models.URLField(
                blank=True,
                null=True,
                max_length=500,
                verbose_name='Canonical URL',
                help_text='Канонический URL страницы (опционально)'
            ),
        ),
        # Мультиязычные поля для AboutPage
        migrations.AddField(
            model_name='aboutpage',
            name='meta_title_uz',
            field=models.CharField(blank=True, null=True, max_length=70, verbose_name='Meta Title'),
        ),
        migrations.AddField(
            model_name='aboutpage',
            name='meta_title_ru',
            field=models.CharField(blank=True, null=True, max_length=70, verbose_name='Meta Title'),
        ),
        migrations.AddField(
            model_name='aboutpage',
            name='meta_title_en',
            field=models.CharField(blank=True, null=True, max_length=70, verbose_name='Meta Title'),
        ),
        migrations.AddField(
            model_name='aboutpage',
            name='meta_description_uz',
            field=models.TextField(blank=True, null=True, max_length=160, verbose_name='Meta Description'),
        ),
        migrations.AddField(
            model_name='aboutpage',
            name='meta_description_ru',
            field=models.TextField(blank=True, null=True, max_length=160, verbose_name='Meta Description'),
        ),
        migrations.AddField(
            model_name='aboutpage',
            name='meta_description_en',
            field=models.TextField(blank=True, null=True, max_length=160, verbose_name='Meta Description'),
        ),
        migrations.AddField(
            model_name='aboutpage',
            name='meta_keywords_uz',
            field=models.CharField(blank=True, null=True, max_length=255, verbose_name='Meta Keywords'),
        ),
        migrations.AddField(
            model_name='aboutpage',
            name='meta_keywords_ru',
            field=models.CharField(blank=True, null=True, max_length=255, verbose_name='Meta Keywords'),
        ),
        migrations.AddField(
            model_name='aboutpage',
            name='meta_keywords_en',
            field=models.CharField(blank=True, null=True, max_length=255, verbose_name='Meta Keywords'),
        ),
        migrations.AddField(
            model_name='aboutpage',
            name='og_title_uz',
            field=models.CharField(blank=True, null=True, max_length=100, verbose_name='OG Title'),
        ),
        migrations.AddField(
            model_name='aboutpage',
            name='og_title_ru',
            field=models.CharField(blank=True, null=True, max_length=100, verbose_name='OG Title'),
        ),
        migrations.AddField(
            model_name='aboutpage',
            name='og_title_en',
            field=models.CharField(blank=True, null=True, max_length=100, verbose_name='OG Title'),
        ),
        migrations.AddField(
            model_name='aboutpage',
            name='og_description_uz',
            field=models.TextField(blank=True, null=True, max_length=200, verbose_name='OG Description'),
        ),
        migrations.AddField(
            model_name='aboutpage',
            name='og_description_ru',
            field=models.TextField(blank=True, null=True, max_length=200, verbose_name='OG Description'),
        ),
        migrations.AddField(
            model_name='aboutpage',
            name='og_description_en',
            field=models.TextField(blank=True, null=True, max_length=200, verbose_name='OG Description'),
        ),
        migrations.AddField(
            model_name='aboutpage',
            name='canonical_url_uz',
            field=models.URLField(blank=True, null=True, max_length=500, verbose_name='Canonical URL'),
        ),
        migrations.AddField(
            model_name='aboutpage',
            name='canonical_url_ru',
            field=models.URLField(blank=True, null=True, max_length=500, verbose_name='Canonical URL'),
        ),
        migrations.AddField(
            model_name='aboutpage',
            name='canonical_url_en',
            field=models.URLField(blank=True, null=True, max_length=500, verbose_name='Canonical URL'),
        ),
        
        # ========== CONTACTPAGE SEO FIELDS ==========
        migrations.AddField(
            model_name='contactpage',
            name='meta_title',
            field=models.CharField(
                blank=True,
                null=True,
                max_length=70,
                verbose_name='Meta Title',
                help_text='Заголовок страницы для поисковых систем (рекомендуется до 60 символов)'
            ),
        ),
        migrations.AddField(
            model_name='contactpage',
            name='meta_description',
            field=models.TextField(
                blank=True,
                null=True,
                max_length=160,
                verbose_name='Meta Description',
                help_text='Описание страницы для поисковых систем (рекомендуется до 160 символов)'
            ),
        ),
        migrations.AddField(
            model_name='contactpage',
            name='meta_keywords',
            field=models.CharField(
                blank=True,
                null=True,
                max_length=255,
                verbose_name='Meta Keywords',
                help_text='Ключевые слова через запятую'
            ),
        ),
        migrations.AddField(
            model_name='contactpage',
            name='og_title',
            field=models.CharField(
                blank=True,
                null=True,
                max_length=100,
                verbose_name='OG Title',
                help_text='Заголовок для социальных сетей (Facebook, Twitter и т.д.)'
            ),
        ),
        migrations.AddField(
            model_name='contactpage',
            name='og_description',
            field=models.TextField(
                blank=True,
                null=True,
                max_length=200,
                verbose_name='OG Description',
                help_text='Описание для социальных сетей'
            ),
        ),
        migrations.AddField(
            model_name='contactpage',
            name='og_image',
            field=models.ImageField(
                blank=True,
                null=True,
                upload_to='photos/seo/%Y/%m/',
                verbose_name='OG Image',
                help_text='Изображение для социальных сетей (рекомендуется 1200x630px)'
            ),
        ),
        migrations.AddField(
            model_name='contactpage',
            name='canonical_url',
            field=models.URLField(
                blank=True,
                null=True,
                max_length=500,
                verbose_name='Canonical URL',
                help_text='Канонический URL страницы (опционально)'
            ),
        ),
        # Мультиязычные поля для ContactPage
        migrations.AddField(
            model_name='contactpage',
            name='meta_title_uz',
            field=models.CharField(blank=True, null=True, max_length=70, verbose_name='Meta Title'),
        ),
        migrations.AddField(
            model_name='contactpage',
            name='meta_title_ru',
            field=models.CharField(blank=True, null=True, max_length=70, verbose_name='Meta Title'),
        ),
        migrations.AddField(
            model_name='contactpage',
            name='meta_title_en',
            field=models.CharField(blank=True, null=True, max_length=70, verbose_name='Meta Title'),
        ),
        migrations.AddField(
            model_name='contactpage',
            name='meta_description_uz',
            field=models.TextField(blank=True, null=True, max_length=160, verbose_name='Meta Description'),
        ),
        migrations.AddField(
            model_name='contactpage',
            name='meta_description_ru',
            field=models.TextField(blank=True, null=True, max_length=160, verbose_name='Meta Description'),
        ),
        migrations.AddField(
            model_name='contactpage',
            name='meta_description_en',
            field=models.TextField(blank=True, null=True, max_length=160, verbose_name='Meta Description'),
        ),
        migrations.AddField(
            model_name='contactpage',
            name='meta_keywords_uz',
            field=models.CharField(blank=True, null=True, max_length=255, verbose_name='Meta Keywords'),
        ),
        migrations.AddField(
            model_name='contactpage',
            name='meta_keywords_ru',
            field=models.CharField(blank=True, null=True, max_length=255, verbose_name='Meta Keywords'),
        ),
        migrations.AddField(
            model_name='contactpage',
            name='meta_keywords_en',
            field=models.CharField(blank=True, null=True, max_length=255, verbose_name='Meta Keywords'),
        ),
        migrations.AddField(
            model_name='contactpage',
            name='og_title_uz',
            field=models.CharField(blank=True, null=True, max_length=100, verbose_name='OG Title'),
        ),
        migrations.AddField(
            model_name='contactpage',
            name='og_title_ru',
            field=models.CharField(blank=True, null=True, max_length=100, verbose_name='OG Title'),
        ),
        migrations.AddField(
            model_name='contactpage',
            name='og_title_en',
            field=models.CharField(blank=True, null=True, max_length=100, verbose_name='OG Title'),
        ),
        migrations.AddField(
            model_name='contactpage',
            name='og_description_uz',
            field=models.TextField(blank=True, null=True, max_length=200, verbose_name='OG Description'),
        ),
        migrations.AddField(
            model_name='contactpage',
            name='og_description_ru',
            field=models.TextField(blank=True, null=True, max_length=200, verbose_name='OG Description'),
        ),
        migrations.AddField(
            model_name='contactpage',
            name='og_description_en',
            field=models.TextField(blank=True, null=True, max_length=200, verbose_name='OG Description'),
        ),
        migrations.AddField(
            model_name='contactpage',
            name='canonical_url_uz',
            field=models.URLField(blank=True, null=True, max_length=500, verbose_name='Canonical URL'),
        ),
        migrations.AddField(
            model_name='contactpage',
            name='canonical_url_ru',
            field=models.URLField(blank=True, null=True, max_length=500, verbose_name='Canonical URL'),
        ),
        migrations.AddField(
            model_name='contactpage',
            name='canonical_url_en',
            field=models.URLField(blank=True, null=True, max_length=500, verbose_name='Canonical URL'),
        ),
    ]
