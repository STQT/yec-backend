# Generated manually

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0036_add_seo_to_carpet_telegram_to_contactpage'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dealerrequest',
            name='message',
            field=models.TextField(
                blank=True,
                help_text='Сообщение от заявителя',
                null=True,
                verbose_name='Текст обращения'
            ),
        ),
    ]
