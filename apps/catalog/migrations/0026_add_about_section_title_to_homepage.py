# Generated manually: add about_section_title field to HomePage

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0025_remove_cta_fields_from_homepage'),
    ]

    operations = [
        migrations.AddField(
            model_name='homepage',
            name='about_section_title',
            field=models.CharField(
                blank=True,
                null=True,
                max_length=200,
                verbose_name='Название секции "О нас"'
            ),
        ),
        # Мультиязычные поля (будут созданы modeltranslation автоматически)
        migrations.AddField(
            model_name='homepage',
            name='about_section_title_uz',
            field=models.CharField(blank=True, null=True, max_length=200, verbose_name='Название секции "О нас"'),
        ),
        migrations.AddField(
            model_name='homepage',
            name='about_section_title_ru',
            field=models.CharField(blank=True, null=True, max_length=200, verbose_name='Название секции "О нас"'),
        ),
        migrations.AddField(
            model_name='homepage',
            name='about_section_title_en',
            field=models.CharField(blank=True, null=True, max_length=200, verbose_name='Название секции "О нас"'),
        ),
    ]
