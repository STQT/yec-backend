# Generated manually: add multilingual fields for cta_contact_link and cta_dealer_link

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("catalog", "0016_update_homepage_fields"),
    ]

    operations = [
        # Добавляем мультиязычные поля для cta_contact_link
        migrations.AddField(
            model_name="homepage",
            name="cta_contact_link_uz",
            field=models.CharField(blank=True, max_length=500, null=True, verbose_name="Ссылка на форму для связи"),
        ),
        migrations.AddField(
            model_name="homepage",
            name="cta_contact_link_ru",
            field=models.CharField(blank=True, max_length=500, null=True, verbose_name="Ссылка на форму для связи"),
        ),
        migrations.AddField(
            model_name="homepage",
            name="cta_contact_link_en",
            field=models.CharField(blank=True, max_length=500, null=True, verbose_name="Ссылка на форму для связи"),
        ),
        # Добавляем мультиязычные поля для cta_dealer_link
        migrations.AddField(
            model_name="homepage",
            name="cta_dealer_link_uz",
            field=models.CharField(blank=True, max_length=500, null=True, verbose_name="Ссылка на форму для становления дилера"),
        ),
        migrations.AddField(
            model_name="homepage",
            name="cta_dealer_link_ru",
            field=models.CharField(blank=True, max_length=500, null=True, verbose_name="Ссылка на форму для становления дилера"),
        ),
        migrations.AddField(
            model_name="homepage",
            name="cta_dealer_link_en",
            field=models.CharField(blank=True, max_length=500, null=True, verbose_name="Ссылка на форму для становления дилера"),
        ),
    ]
