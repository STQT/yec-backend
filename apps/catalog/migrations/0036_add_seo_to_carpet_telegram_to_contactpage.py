# Generated manually

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0035_globalsettings_dealer_form_description_and_more'),
    ]

    operations = [
        # Carpet SEO fields
        migrations.AddField(
            model_name='carpet',
            name='seo_description',
            field=models.TextField(blank=True, help_text='Описание страницы для поисковых систем (рекомендуется до 160 символов)', max_length=160, null=True, verbose_name='SEO Description'),
        ),
        migrations.AddField(
            model_name='carpet',
            name='seo_description_en',
            field=models.TextField(blank=True, help_text='Описание страницы для поисковых систем (рекомендуется до 160 символов)', max_length=160, null=True, verbose_name='SEO Description'),
        ),
        migrations.AddField(
            model_name='carpet',
            name='seo_description_ru',
            field=models.TextField(blank=True, help_text='Описание страницы для поисковых систем (рекомендуется до 160 символов)', max_length=160, null=True, verbose_name='SEO Description'),
        ),
        migrations.AddField(
            model_name='carpet',
            name='seo_description_uz',
            field=models.TextField(blank=True, help_text='Описание страницы для поисковых систем (рекомендуется до 160 символов)', max_length=160, null=True, verbose_name='SEO Description'),
        ),
        migrations.AddField(
            model_name='carpet',
            name='seo_title',
            field=models.CharField(blank=True, help_text='Заголовок страницы для поисковых систем (рекомендуется до 60 символов)', max_length=70, null=True, verbose_name='SEO Title'),
        ),
        migrations.AddField(
            model_name='carpet',
            name='seo_title_en',
            field=models.CharField(blank=True, help_text='Заголовок страницы для поисковых систем (рекомендуется до 60 символов)', max_length=70, null=True, verbose_name='SEO Title'),
        ),
        migrations.AddField(
            model_name='carpet',
            name='seo_title_ru',
            field=models.CharField(blank=True, help_text='Заголовок страницы для поисковых систем (рекомендуется до 60 символов)', max_length=70, null=True, verbose_name='SEO Title'),
        ),
        migrations.AddField(
            model_name='carpet',
            name='seo_title_uz',
            field=models.CharField(blank=True, help_text='Заголовок страницы для поисковых систем (рекомендуется до 60 символов)', max_length=70, null=True, verbose_name='SEO Title'),
        ),
        # ContactPage telegram_url
        migrations.AddField(
            model_name='contactpage',
            name='telegram_url',
            field=models.URLField(blank=True, null=True, verbose_name='Telegram'),
        ),
    ]
