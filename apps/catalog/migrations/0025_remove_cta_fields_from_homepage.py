# Generated manually: remove CTA (Call to Action) fields from HomePage

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0024_alter_companyhistory_options_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='homepage',
            name='cta_contact_link',
        ),
        migrations.RemoveField(
            model_name='homepage',
            name='cta_dealer_link',
        ),
        migrations.RemoveField(
            model_name='homepage',
            name='cta_description',
        ),
        migrations.RemoveField(
            model_name='homepage',
            name='cta_image',
        ),
        migrations.RemoveField(
            model_name='homepage',
            name='cta_title',
        ),
        # Удаляем мультиязычные поля
        migrations.RemoveField(
            model_name='homepage',
            name='cta_contact_link_uz',
        ),
        migrations.RemoveField(
            model_name='homepage',
            name='cta_contact_link_ru',
        ),
        migrations.RemoveField(
            model_name='homepage',
            name='cta_contact_link_en',
        ),
        migrations.RemoveField(
            model_name='homepage',
            name='cta_dealer_link_uz',
        ),
        migrations.RemoveField(
            model_name='homepage',
            name='cta_dealer_link_ru',
        ),
        migrations.RemoveField(
            model_name='homepage',
            name='cta_dealer_link_en',
        ),
        migrations.RemoveField(
            model_name='homepage',
            name='cta_description_uz',
        ),
        migrations.RemoveField(
            model_name='homepage',
            name='cta_description_ru',
        ),
        migrations.RemoveField(
            model_name='homepage',
            name='cta_description_en',
        ),
        migrations.RemoveField(
            model_name='homepage',
            name='cta_title_uz',
        ),
        migrations.RemoveField(
            model_name='homepage',
            name='cta_title_ru',
        ),
        migrations.RemoveField(
            model_name='homepage',
            name='cta_title_en',
        ),
    ]
