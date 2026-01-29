# Generated manually: update HomePage model - add AboutImage model, remove old image fields, add new fields

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("catalog", "0015_rework_maingallery_singleton"),
    ]

    operations = [
        # Создаем модель AboutImage
        migrations.CreateModel(
            name="AboutImage",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("image", models.ImageField(upload_to="photos/homepage/about/%Y/%m/", verbose_name="Изображение")),
                ("order", models.PositiveIntegerField(default=0, verbose_name="Порядок сортировки")),
                (
                    "homepage",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="about_images",
                        to="catalog.homepage",
                        verbose_name="Главная страница",
                    ),
                ),
            ],
            options={
                "verbose_name": 'Изображение секции "О нас"',
                "verbose_name_plural": 'Изображения секции "О нас"',
                "ordering": ["order"],
            },
        ),
        # Удаляем старые поля изображений из HomePage
        migrations.RemoveField(
            model_name="homepage",
            name="about_image_1",
        ),
        migrations.RemoveField(
            model_name="homepage",
            name="about_image_2",
        ),
        migrations.RemoveField(
            model_name="homepage",
            name="about_image_3",
        ),
        # Удаляем поле showroom_link
        migrations.RemoveField(
            model_name="homepage",
            name="showroom_link",
        ),
        # Добавляем новые поля в секцию Преимущества (nullable для совместимости)
        migrations.AddField(
            model_name="homepage",
            name="advantage_title",
            field=models.CharField(blank=True, max_length=200, null=True, verbose_name="Заголовок секции преимуществ"),
        ),
        migrations.AddField(
            model_name="homepage",
            name="advantage_subtitle",
            field=models.CharField(blank=True, max_length=200, null=True, verbose_name="Подзаголовок секции преимуществ"),
        ),
        # Добавляем поле изображения в секцию CTA
        migrations.AddField(
            model_name="homepage",
            name="cta_image",
            field=models.ImageField(
                blank=True, null=True, upload_to="photos/homepage/cta/%Y/%m/", verbose_name="Изображение призыва к действию"
            ),
        ),
        # Добавляем мультиязычные поля для advantage_title и advantage_subtitle
        migrations.AddField(
            model_name="homepage",
            name="advantage_title_uz",
            field=models.CharField(max_length=200, null=True, verbose_name="Заголовок секции преимуществ"),
        ),
        migrations.AddField(
            model_name="homepage",
            name="advantage_title_ru",
            field=models.CharField(max_length=200, null=True, verbose_name="Заголовок секции преимуществ"),
        ),
        migrations.AddField(
            model_name="homepage",
            name="advantage_title_en",
            field=models.CharField(max_length=200, null=True, verbose_name="Заголовок секции преимуществ"),
        ),
        migrations.AddField(
            model_name="homepage",
            name="advantage_subtitle_uz",
            field=models.CharField(max_length=200, null=True, verbose_name="Подзаголовок секции преимуществ"),
        ),
        migrations.AddField(
            model_name="homepage",
            name="advantage_subtitle_ru",
            field=models.CharField(max_length=200, null=True, verbose_name="Подзаголовок секции преимуществ"),
        ),
        migrations.AddField(
            model_name="homepage",
            name="advantage_subtitle_en",
            field=models.CharField(max_length=200, null=True, verbose_name="Подзаголовок секции преимуществ"),
        ),
    ]
