# Generated manually: add image field to CompanyHistory

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0022_add_seo_fields'),
    ]

    operations = [
        migrations.AddField(
            model_name='companyhistory',
            name='image',
            field=models.ImageField(
                blank=True,
                null=True,
                upload_to='photos/company_history/%Y/%m/',
                verbose_name='Изображение'
            ),
        ),
    ]
