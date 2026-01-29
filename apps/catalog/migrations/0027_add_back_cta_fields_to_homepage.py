# Generated manually: add back CTA fields (title, description, image) to HomePage

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0026_add_about_section_title_to_homepage'),
    ]

    operations = [
        migrations.AddField(
            model_name='homepage',
            name='cta_title',
            field=models.CharField(
                max_length=200,
                null=True,
                verbose_name='Заголовок призыва к действию'
            ),
        ),
        migrations.AddField(
            model_name='homepage',
            name='cta_description',
            field=models.TextField(
                null=True,
                verbose_name='Описание призыва к действию'
            ),
        ),
        migrations.AddField(
            model_name='homepage',
            name='cta_image',
            field=models.ImageField(
                blank=True,
                null=True,
                upload_to='photos/homepage/cta/%Y/%m/',
                verbose_name='Изображение призыва к действию'
            ),
        ),
        # Мультиязычные поля (будут созданы modeltranslation автоматически)
        migrations.AddField(
            model_name='homepage',
            name='cta_title_uz',
            field=models.CharField(max_length=200, null=True, verbose_name='Заголовок призыва к действию'),
        ),
        migrations.AddField(
            model_name='homepage',
            name='cta_title_ru',
            field=models.CharField(max_length=200, null=True, verbose_name='Заголовок призыва к действию'),
        ),
        migrations.AddField(
            model_name='homepage',
            name='cta_title_en',
            field=models.CharField(max_length=200, null=True, verbose_name='Заголовок призыва к действию'),
        ),
        migrations.AddField(
            model_name='homepage',
            name='cta_description_uz',
            field=models.TextField(null=True, verbose_name='Описание призыва к действию'),
        ),
        migrations.AddField(
            model_name='homepage',
            name='cta_description_ru',
            field=models.TextField(null=True, verbose_name='Описание призыва к действию'),
        ),
        migrations.AddField(
            model_name='homepage',
            name='cta_description_en',
            field=models.TextField(null=True, verbose_name='Описание призыва к действию'),
        ),
    ]
