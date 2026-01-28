# Generated manually: rework MainGallery to singleton with 12 fixed images + translated title

from django.db import migrations, models


def create_initial_main_gallery(apps, schema_editor):
    MainGallery = apps.get_model("catalog", "MainGallery")
    MainGallery.objects.all().delete()
    MainGallery.objects.create(
        title="Shourumni onlayn tomosha qiling",
        title_uz="Shourumni onlayn tomosha qiling",
        title_ru="Смотрите шоурум онлайн",
        title_en="Watch the showroom online",
    )


def reverse_create_initial_main_gallery(apps, schema_editor):
    MainGallery = apps.get_model("catalog", "MainGallery")
    MainGallery.objects.all().delete()


class Migration(migrations.Migration):
    dependencies = [
        ("catalog", "0014_remove_pointtype"),
    ]

    operations = [
        migrations.DeleteModel(name="MainGallery"),
        migrations.CreateModel(
            name="MainGallery",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("title", models.CharField(max_length=200, verbose_name="Заголовок")),
                ("title_uz", models.CharField(max_length=200, null=True, verbose_name="Заголовок")),
                ("title_ru", models.CharField(max_length=200, null=True, verbose_name="Заголовок")),
                ("title_en", models.CharField(max_length=200, null=True, verbose_name="Заголовок")),
                ("image_1", models.ImageField(blank=True, null=True, upload_to="photos/main_gallery/%Y/%m/", verbose_name="Изображение 1")),
                ("image_2", models.ImageField(blank=True, null=True, upload_to="photos/main_gallery/%Y/%m/", verbose_name="Изображение 2")),
                ("image_3", models.ImageField(blank=True, null=True, upload_to="photos/main_gallery/%Y/%m/", verbose_name="Изображение 3")),
                ("image_4", models.ImageField(blank=True, null=True, upload_to="photos/main_gallery/%Y/%m/", verbose_name="Изображение 4")),
                ("image_5", models.ImageField(blank=True, null=True, upload_to="photos/main_gallery/%Y/%m/", verbose_name="Изображение 5")),
                ("image_6", models.ImageField(blank=True, null=True, upload_to="photos/main_gallery/%Y/%m/", verbose_name="Изображение 6")),
                ("image_7", models.ImageField(blank=True, null=True, upload_to="photos/main_gallery/%Y/%m/", verbose_name="Изображение 7")),
                ("image_8", models.ImageField(blank=True, null=True, upload_to="photos/main_gallery/%Y/%m/", verbose_name="Изображение 8")),
                ("image_9", models.ImageField(blank=True, null=True, upload_to="photos/main_gallery/%Y/%m/", verbose_name="Изображение 9")),
                ("image_10", models.ImageField(blank=True, null=True, upload_to="photos/main_gallery/%Y/%m/", verbose_name="Изображение 10")),
                ("image_11", models.ImageField(blank=True, null=True, upload_to="photos/main_gallery/%Y/%m/", verbose_name="Изображение 11")),
                ("image_12", models.ImageField(blank=True, null=True, upload_to="photos/main_gallery/%Y/%m/", verbose_name="Изображение 12")),
                ("created_at", models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")),
                ("update_at", models.DateTimeField(auto_now=True, verbose_name="Дата обновления")),
            ],
            options={
                "verbose_name": "Нижняя галерея",
                "verbose_name_plural": "Нижняя галерея",
            },
        ),
        migrations.RunPython(create_initial_main_gallery, reverse_create_initial_main_gallery),
    ]

