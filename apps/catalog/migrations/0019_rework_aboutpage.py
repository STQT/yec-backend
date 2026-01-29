# Generated manually: rework AboutPage model according to new structure

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("catalog", "0018_remove_banner_showroom_link"),
    ]

    operations = [
        # ========== УДАЛЕНИЕ СТАРЫХ ПОЛЕЙ ИЗ AboutPage ==========
        migrations.RemoveField(
            model_name="aboutpage",
            name="company_title",
        ),
        migrations.RemoveField(
            model_name="aboutpage",
            name="company_subtitle",
        ),
        migrations.RemoveField(
            model_name="aboutpage",
            name="company_description",
        ),
        migrations.RemoveField(
            model_name="aboutpage",
            name="main_image",
        ),
        migrations.RemoveField(
            model_name="aboutpage",
            name="showroom_image",
        ),
        migrations.RemoveField(
            model_name="aboutpage",
            name="showroom_button_text",
        ),
        
        # ========== ДОБАВЛЕНИЕ НОВЫХ ПОЛЕЙ В AboutPage ==========
        # Секция 1: О компании
        migrations.AddField(
            model_name="aboutpage",
            name="about_section_title",
            field=models.CharField(blank=True, null=True, max_length=200, verbose_name='Название секции "О компании"'),
        ),
        migrations.AddField(
            model_name="aboutpage",
            name="about_banner_title",
            field=models.CharField(blank=True, null=True, max_length=200, verbose_name='Заголовок баннера'),
        ),
        migrations.AddField(
            model_name="aboutpage",
            name="about_banner_subtitle",
            field=models.CharField(blank=True, null=True, max_length=200, verbose_name='Подзаголовок баннера'),
        ),
        migrations.AddField(
            model_name="aboutpage",
            name="about_image_1",
            field=models.ImageField(blank=True, null=True, upload_to='photos/about/%Y/%m/', verbose_name='Изображение 1'),
        ),
        migrations.AddField(
            model_name="aboutpage",
            name="about_image_2",
            field=models.ImageField(blank=True, null=True, upload_to='photos/about/%Y/%m/', verbose_name='Изображение 2'),
        ),
        
        # Секция 2: Процесс производства
        migrations.AddField(
            model_name="aboutpage",
            name="production_title",
            field=models.CharField(blank=True, null=True, max_length=200, verbose_name='Заголовок секции производства'),
        ),
        
        # Секция 4: Объемы производства
        migrations.AddField(
            model_name="aboutpage",
            name="capacity_title",
            field=models.CharField(blank=True, null=True, max_length=200, verbose_name='Заголовок секции объемов'),
        ),
        # Карточка 1
        migrations.AddField(
            model_name="aboutpage",
            name="capacity_card_1_title",
            field=models.CharField(blank=True, null=True, max_length=200, verbose_name='Заголовок карточки 1'),
        ),
        migrations.AddField(
            model_name="aboutpage",
            name="capacity_card_1_subtitle",
            field=models.CharField(blank=True, null=True, max_length=200, verbose_name='Подзаголовок карточки 1'),
        ),
        migrations.AddField(
            model_name="aboutpage",
            name="capacity_card_1_image",
            field=models.ImageField(blank=True, null=True, upload_to='photos/production_capacity/%Y/%m/', verbose_name='Изображение карточки 1'),
        ),
        # Карточка 2
        migrations.AddField(
            model_name="aboutpage",
            name="capacity_card_2_title",
            field=models.CharField(blank=True, null=True, max_length=200, verbose_name='Заголовок карточки 2'),
        ),
        migrations.AddField(
            model_name="aboutpage",
            name="capacity_card_2_subtitle",
            field=models.CharField(blank=True, null=True, max_length=200, verbose_name='Подзаголовок карточки 2'),
        ),
        migrations.AddField(
            model_name="aboutpage",
            name="capacity_card_2_image",
            field=models.ImageField(blank=True, null=True, upload_to='photos/production_capacity/%Y/%m/', verbose_name='Изображение карточки 2'),
        ),
        # Карточка 3
        migrations.AddField(
            model_name="aboutpage",
            name="capacity_card_3_title",
            field=models.CharField(blank=True, null=True, max_length=200, verbose_name='Заголовок карточки 3'),
        ),
        migrations.AddField(
            model_name="aboutpage",
            name="capacity_card_3_subtitle",
            field=models.CharField(blank=True, null=True, max_length=200, verbose_name='Подзаголовок карточки 3'),
        ),
        migrations.AddField(
            model_name="aboutpage",
            name="capacity_card_3_image",
            field=models.ImageField(blank=True, null=True, upload_to='photos/production_capacity/%Y/%m/', verbose_name='Изображение карточки 3'),
        ),
        # Карточка 4
        migrations.AddField(
            model_name="aboutpage",
            name="capacity_card_4_title",
            field=models.CharField(blank=True, null=True, max_length=200, verbose_name='Заголовок карточки 4'),
        ),
        migrations.AddField(
            model_name="aboutpage",
            name="capacity_card_4_subtitle",
            field=models.CharField(blank=True, null=True, max_length=200, verbose_name='Подзаголовок карточки 4'),
        ),
        migrations.AddField(
            model_name="aboutpage",
            name="capacity_card_4_image",
            field=models.ImageField(blank=True, null=True, upload_to='photos/production_capacity/%Y/%m/', verbose_name='Изображение карточки 4'),
        ),
        
        # Секция 5: Партнерство для дилеров
        migrations.AddField(
            model_name="aboutpage",
            name="dealer_title",
            field=models.CharField(blank=True, null=True, max_length=200, verbose_name='Заголовок секции для дилеров'),
        ),
        # Карточка 1
        migrations.AddField(
            model_name="aboutpage",
            name="dealer_card_1_title",
            field=models.CharField(blank=True, null=True, max_length=200, verbose_name='Заголовок карточки 1'),
        ),
        migrations.AddField(
            model_name="aboutpage",
            name="dealer_card_1_description",
            field=models.TextField(blank=True, null=True, verbose_name='Описание карточки 1'),
        ),
        # Карточка 2
        migrations.AddField(
            model_name="aboutpage",
            name="dealer_card_2_title",
            field=models.CharField(blank=True, null=True, max_length=200, verbose_name='Заголовок карточки 2'),
        ),
        migrations.AddField(
            model_name="aboutpage",
            name="dealer_card_2_description",
            field=models.TextField(blank=True, null=True, verbose_name='Описание карточки 2'),
        ),
        # Карточка 3
        migrations.AddField(
            model_name="aboutpage",
            name="dealer_card_3_title",
            field=models.CharField(blank=True, null=True, max_length=200, verbose_name='Заголовок карточки 3'),
        ),
        migrations.AddField(
            model_name="aboutpage",
            name="dealer_card_3_description",
            field=models.TextField(blank=True, null=True, verbose_name='Описание карточки 3'),
        ),
        
        # ========== ОБНОВЛЕНИЕ CompanyHistory ==========
        migrations.RemoveField(
            model_name="companyhistory",
            name="image",
        ),
        migrations.RemoveField(
            model_name="companyhistory",
            name="order",
        ),
        migrations.RenameField(
            model_name="companyhistory",
            old_name="title",
            new_name="year_title",
        ),
        migrations.RenameField(
            model_name="companyhistory",
            old_name="description",
            new_name="year_description",
        ),
        
        # ========== УДАЛЕНИЕ МОДЕЛЕЙ ==========
        migrations.DeleteModel(
            name="ProductionCapacity",
        ),
        migrations.DeleteModel(
            name="DealerAdvantage",
        ),
        
        # ========== ДОБАВЛЕНИЕ МУЛЬТИЯЗЫЧНЫХ ПОЛЕЙ ==========
        # Секция 1: О компании
        migrations.AddField(
            model_name="aboutpage",
            name="about_section_title_uz",
            field=models.CharField(max_length=200, null=True, verbose_name='Название секции "О компании"'),
        ),
        migrations.AddField(
            model_name="aboutpage",
            name="about_section_title_ru",
            field=models.CharField(max_length=200, null=True, verbose_name='Название секции "О компании"'),
        ),
        migrations.AddField(
            model_name="aboutpage",
            name="about_section_title_en",
            field=models.CharField(max_length=200, null=True, verbose_name='Название секции "О компании"'),
        ),
        migrations.AddField(
            model_name="aboutpage",
            name="about_banner_title_uz",
            field=models.CharField(max_length=200, null=True, verbose_name='Заголовок баннера'),
        ),
        migrations.AddField(
            model_name="aboutpage",
            name="about_banner_title_ru",
            field=models.CharField(max_length=200, null=True, verbose_name='Заголовок баннера'),
        ),
        migrations.AddField(
            model_name="aboutpage",
            name="about_banner_title_en",
            field=models.CharField(max_length=200, null=True, verbose_name='Заголовок баннера'),
        ),
        migrations.AddField(
            model_name="aboutpage",
            name="about_banner_subtitle_uz",
            field=models.CharField(max_length=200, null=True, verbose_name='Подзаголовок баннера'),
        ),
        migrations.AddField(
            model_name="aboutpage",
            name="about_banner_subtitle_ru",
            field=models.CharField(max_length=200, null=True, verbose_name='Подзаголовок баннера'),
        ),
        migrations.AddField(
            model_name="aboutpage",
            name="about_banner_subtitle_en",
            field=models.CharField(max_length=200, null=True, verbose_name='Подзаголовок баннера'),
        ),
        
        # Секция 2: Процесс производства
        migrations.AddField(
            model_name="aboutpage",
            name="production_title_uz",
            field=models.CharField(max_length=200, null=True, verbose_name='Заголовок секции производства'),
        ),
        migrations.AddField(
            model_name="aboutpage",
            name="production_title_ru",
            field=models.CharField(max_length=200, null=True, verbose_name='Заголовок секции производства'),
        ),
        migrations.AddField(
            model_name="aboutpage",
            name="production_title_en",
            field=models.CharField(max_length=200, null=True, verbose_name='Заголовок секции производства'),
        ),
        
        # Секция 4: Объемы производства
        migrations.AddField(
            model_name="aboutpage",
            name="capacity_title_uz",
            field=models.CharField(max_length=200, null=True, verbose_name='Заголовок секции объемов'),
        ),
        migrations.AddField(
            model_name="aboutpage",
            name="capacity_title_ru",
            field=models.CharField(max_length=200, null=True, verbose_name='Заголовок секции объемов'),
        ),
        migrations.AddField(
            model_name="aboutpage",
            name="capacity_title_en",
            field=models.CharField(max_length=200, null=True, verbose_name='Заголовок секции объемов'),
        ),
        migrations.AddField(
            model_name="aboutpage",
            name="capacity_card_1_title_uz",
            field=models.CharField(max_length=200, null=True, verbose_name='Заголовок карточки 1'),
        ),
        migrations.AddField(
            model_name="aboutpage",
            name="capacity_card_1_title_ru",
            field=models.CharField(max_length=200, null=True, verbose_name='Заголовок карточки 1'),
        ),
        migrations.AddField(
            model_name="aboutpage",
            name="capacity_card_1_title_en",
            field=models.CharField(max_length=200, null=True, verbose_name='Заголовок карточки 1'),
        ),
        migrations.AddField(
            model_name="aboutpage",
            name="capacity_card_1_subtitle_uz",
            field=models.CharField(max_length=200, null=True, verbose_name='Подзаголовок карточки 1'),
        ),
        migrations.AddField(
            model_name="aboutpage",
            name="capacity_card_1_subtitle_ru",
            field=models.CharField(max_length=200, null=True, verbose_name='Подзаголовок карточки 1'),
        ),
        migrations.AddField(
            model_name="aboutpage",
            name="capacity_card_1_subtitle_en",
            field=models.CharField(max_length=200, null=True, verbose_name='Подзаголовок карточки 1'),
        ),
        migrations.AddField(
            model_name="aboutpage",
            name="capacity_card_2_title_uz",
            field=models.CharField(max_length=200, null=True, verbose_name='Заголовок карточки 2'),
        ),
        migrations.AddField(
            model_name="aboutpage",
            name="capacity_card_2_title_ru",
            field=models.CharField(max_length=200, null=True, verbose_name='Заголовок карточки 2'),
        ),
        migrations.AddField(
            model_name="aboutpage",
            name="capacity_card_2_title_en",
            field=models.CharField(max_length=200, null=True, verbose_name='Заголовок карточки 2'),
        ),
        migrations.AddField(
            model_name="aboutpage",
            name="capacity_card_2_subtitle_uz",
            field=models.CharField(max_length=200, null=True, verbose_name='Подзаголовок карточки 2'),
        ),
        migrations.AddField(
            model_name="aboutpage",
            name="capacity_card_2_subtitle_ru",
            field=models.CharField(max_length=200, null=True, verbose_name='Подзаголовок карточки 2'),
        ),
        migrations.AddField(
            model_name="aboutpage",
            name="capacity_card_2_subtitle_en",
            field=models.CharField(max_length=200, null=True, verbose_name='Подзаголовок карточки 2'),
        ),
        migrations.AddField(
            model_name="aboutpage",
            name="capacity_card_3_title_uz",
            field=models.CharField(max_length=200, null=True, verbose_name='Заголовок карточки 3'),
        ),
        migrations.AddField(
            model_name="aboutpage",
            name="capacity_card_3_title_ru",
            field=models.CharField(max_length=200, null=True, verbose_name='Заголовок карточки 3'),
        ),
        migrations.AddField(
            model_name="aboutpage",
            name="capacity_card_3_title_en",
            field=models.CharField(max_length=200, null=True, verbose_name='Заголовок карточки 3'),
        ),
        migrations.AddField(
            model_name="aboutpage",
            name="capacity_card_3_subtitle_uz",
            field=models.CharField(max_length=200, null=True, verbose_name='Подзаголовок карточки 3'),
        ),
        migrations.AddField(
            model_name="aboutpage",
            name="capacity_card_3_subtitle_ru",
            field=models.CharField(max_length=200, null=True, verbose_name='Подзаголовок карточки 3'),
        ),
        migrations.AddField(
            model_name="aboutpage",
            name="capacity_card_3_subtitle_en",
            field=models.CharField(max_length=200, null=True, verbose_name='Подзаголовок карточки 3'),
        ),
        migrations.AddField(
            model_name="aboutpage",
            name="capacity_card_4_title_uz",
            field=models.CharField(max_length=200, null=True, verbose_name='Заголовок карточки 4'),
        ),
        migrations.AddField(
            model_name="aboutpage",
            name="capacity_card_4_title_ru",
            field=models.CharField(max_length=200, null=True, verbose_name='Заголовок карточки 4'),
        ),
        migrations.AddField(
            model_name="aboutpage",
            name="capacity_card_4_title_en",
            field=models.CharField(max_length=200, null=True, verbose_name='Заголовок карточки 4'),
        ),
        migrations.AddField(
            model_name="aboutpage",
            name="capacity_card_4_subtitle_uz",
            field=models.CharField(max_length=200, null=True, verbose_name='Подзаголовок карточки 4'),
        ),
        migrations.AddField(
            model_name="aboutpage",
            name="capacity_card_4_subtitle_ru",
            field=models.CharField(max_length=200, null=True, verbose_name='Подзаголовок карточки 4'),
        ),
        migrations.AddField(
            model_name="aboutpage",
            name="capacity_card_4_subtitle_en",
            field=models.CharField(max_length=200, null=True, verbose_name='Подзаголовок карточки 4'),
        ),
        
        # Секция 5: Партнерство для дилеров
        migrations.AddField(
            model_name="aboutpage",
            name="dealer_title_uz",
            field=models.CharField(max_length=200, null=True, verbose_name='Заголовок секции для дилеров'),
        ),
        migrations.AddField(
            model_name="aboutpage",
            name="dealer_title_ru",
            field=models.CharField(max_length=200, null=True, verbose_name='Заголовок секции для дилеров'),
        ),
        migrations.AddField(
            model_name="aboutpage",
            name="dealer_title_en",
            field=models.CharField(max_length=200, null=True, verbose_name='Заголовок секции для дилеров'),
        ),
        migrations.AddField(
            model_name="aboutpage",
            name="dealer_card_1_title_uz",
            field=models.CharField(max_length=200, null=True, verbose_name='Заголовок карточки 1'),
        ),
        migrations.AddField(
            model_name="aboutpage",
            name="dealer_card_1_title_ru",
            field=models.CharField(max_length=200, null=True, verbose_name='Заголовок карточки 1'),
        ),
        migrations.AddField(
            model_name="aboutpage",
            name="dealer_card_1_title_en",
            field=models.CharField(max_length=200, null=True, verbose_name='Заголовок карточки 1'),
        ),
        migrations.AddField(
            model_name="aboutpage",
            name="dealer_card_1_description_uz",
            field=models.TextField(null=True, verbose_name='Описание карточки 1'),
        ),
        migrations.AddField(
            model_name="aboutpage",
            name="dealer_card_1_description_ru",
            field=models.TextField(null=True, verbose_name='Описание карточки 1'),
        ),
        migrations.AddField(
            model_name="aboutpage",
            name="dealer_card_1_description_en",
            field=models.TextField(null=True, verbose_name='Описание карточки 1'),
        ),
        migrations.AddField(
            model_name="aboutpage",
            name="dealer_card_2_title_uz",
            field=models.CharField(max_length=200, null=True, verbose_name='Заголовок карточки 2'),
        ),
        migrations.AddField(
            model_name="aboutpage",
            name="dealer_card_2_title_ru",
            field=models.CharField(max_length=200, null=True, verbose_name='Заголовок карточки 2'),
        ),
        migrations.AddField(
            model_name="aboutpage",
            name="dealer_card_2_title_en",
            field=models.CharField(max_length=200, null=True, verbose_name='Заголовок карточки 2'),
        ),
        migrations.AddField(
            model_name="aboutpage",
            name="dealer_card_2_description_uz",
            field=models.TextField(null=True, verbose_name='Описание карточки 2'),
        ),
        migrations.AddField(
            model_name="aboutpage",
            name="dealer_card_2_description_ru",
            field=models.TextField(null=True, verbose_name='Описание карточки 2'),
        ),
        migrations.AddField(
            model_name="aboutpage",
            name="dealer_card_2_description_en",
            field=models.TextField(null=True, verbose_name='Описание карточки 2'),
        ),
        migrations.AddField(
            model_name="aboutpage",
            name="dealer_card_3_title_uz",
            field=models.CharField(max_length=200, null=True, verbose_name='Заголовок карточки 3'),
        ),
        migrations.AddField(
            model_name="aboutpage",
            name="dealer_card_3_title_ru",
            field=models.CharField(max_length=200, null=True, verbose_name='Заголовок карточки 3'),
        ),
        migrations.AddField(
            model_name="aboutpage",
            name="dealer_card_3_title_en",
            field=models.CharField(max_length=200, null=True, verbose_name='Заголовок карточки 3'),
        ),
        migrations.AddField(
            model_name="aboutpage",
            name="dealer_card_3_description_uz",
            field=models.TextField(null=True, verbose_name='Описание карточки 3'),
        ),
        migrations.AddField(
            model_name="aboutpage",
            name="dealer_card_3_description_ru",
            field=models.TextField(null=True, verbose_name='Описание карточки 3'),
        ),
        migrations.AddField(
            model_name="aboutpage",
            name="dealer_card_3_description_en",
            field=models.TextField(null=True, verbose_name='Описание карточки 3'),
        ),
        
        # CompanyHistory мультиязычные поля
        migrations.AddField(
            model_name="companyhistory",
            name="year_title_uz",
            field=models.CharField(max_length=200, null=True, verbose_name='Название года'),
        ),
        migrations.AddField(
            model_name="companyhistory",
            name="year_title_ru",
            field=models.CharField(max_length=200, null=True, verbose_name='Название года'),
        ),
        migrations.AddField(
            model_name="companyhistory",
            name="year_title_en",
            field=models.CharField(max_length=200, null=True, verbose_name='Название года'),
        ),
        migrations.AddField(
            model_name="companyhistory",
            name="year_description_uz",
            field=models.TextField(null=True, verbose_name='Описание года'),
        ),
        migrations.AddField(
            model_name="companyhistory",
            name="year_description_ru",
            field=models.TextField(null=True, verbose_name='Описание года'),
        ),
        migrations.AddField(
            model_name="companyhistory",
            name="year_description_en",
            field=models.TextField(null=True, verbose_name='Описание года'),
        ),
    ]


