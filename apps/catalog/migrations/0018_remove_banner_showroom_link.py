# Generated manually: remove banner_showroom_link field and its multilingual versions

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("catalog", "0017_add_multilang_cta_links"),
    ]

    operations = [
        # Удаляем мультиязычные поля для banner_showroom_link
        migrations.RemoveField(
            model_name="homepage",
            name="banner_showroom_link_uz",
        ),
        migrations.RemoveField(
            model_name="homepage",
            name="banner_showroom_link_ru",
        ),
        migrations.RemoveField(
            model_name="homepage",
            name="banner_showroom_link_en",
        ),
        # Удаляем основное поле banner_showroom_link
        migrations.RemoveField(
            model_name="homepage",
            name="banner_showroom_link",
        ),
    ]
