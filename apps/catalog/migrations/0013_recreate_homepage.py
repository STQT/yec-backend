# Generated manually for recreating HomePage model

from django.db import migrations, models


def create_initial_homepage(apps, schema_editor):
    """Создание начальной записи HomePage с данными из скриншотов"""
    HomePage = apps.get_model('catalog', 'HomePage')
    
    # Удаляем старые записи, если есть
    HomePage.objects.all().delete()
    
    # Создаем новую запись с данными из скриншотов
    HomePage.objects.create(
        # Секция 1: Баннер
        banner_title_uz="Soddalik va nafislilik uyg'unligi",
        banner_title_ru="Гармония простоты и изысканности",
        banner_title_en="Harmony of simplicity and elegance",
        banner_description_uz="Uyingizga iliqlik va zamonaviy ko'rinish beruvchi yuqori sifatli gilamlar. Nozik dizayn va mustahkam materiallar — barchasi siz uchun.",
        banner_description_ru="Высококачественные ковры, придающие тепло и современный вид вашему дому. Изысканный дизайн и прочные материалы — всё для вас.",
        banner_description_en="High-quality carpets that add warmth and modern look to your home. Elegant design and durable materials — everything for you.",
        banner_link_uz="",
        banner_link_ru="",
        banner_link_en="",
        banner_showroom_title_uz="Gilamlarni onlayn tomosha qiling",
        banner_showroom_title_ru="Смотрите ковры онлайн",
        banner_showroom_title_en="Watch carpets online",
        banner_showroom_link_uz="",
        banner_showroom_link_ru="",
        banner_showroom_link_en="",
        
        # Секция 2: О нас
        about_title_uz="BIZ HAQIMIZDA",
        about_title_ru="О НАС",
        about_title_en="ABOUT US",
        about_link_uz="",
        about_link_ru="",
        about_link_en="",
        about_youtube_link_uz="",
        about_youtube_link_ru="",
        about_youtube_link_en="",
        about_bottom_description_uz="YEC yangi kolleksiyalarni taqdim etadi. Mahsulotlarimiz ko'plab mamlakatlarga eksport qilinmoqda.",
        about_bottom_description_ru="YEC представляет новые коллекции. Наша продукция экспортируется во многие страны.",
        about_bottom_description_en="YEC presents new collections. Our products are exported to many countries.",
        
        # Секция 3: Шоурум
        showroom_title_uz="Shourumni onlayn tomosha qiling",
        showroom_title_ru="Смотрите шоурум онлайн",
        showroom_title_en="Watch the showroom online",
        showroom_link_uz="",
        showroom_link_ru="",
        showroom_link_en="",
        
        # Секция 4: Преимущества
        advantage_1_title_uz="Yuqori sifat gulamlar",
        advantage_1_title_ru="Высококачественные ковры",
        advantage_1_title_en="High quality carpets",
        advantage_1_description_uz="Milliy va zamonaviy dizayn uyg'unligidagi eksklyuziv kolleksiyalar",
        advantage_1_description_ru="Эксклюзивные коллекции в гармонии национального и современного дизайна",
        advantage_1_description_en="Exclusive collections in harmony of national and modern design",
        
        advantage_2_title_uz="Noyob naqshli gulamlar",
        advantage_2_title_ru="Ковры с уникальными узорами",
        advantage_2_title_en="Unique patterned carpets",
        advantage_2_description_uz="Milliy va zamonaviy dizayn uyg'unligidagi eksklyuziv kolleksiyalar",
        advantage_2_description_ru="Эксклюзивные коллекции в гармонии национального и современного дизайна",
        advantage_2_description_en="Exclusive collections in harmony of national and modern design",
        
        advantage_3_title_uz="Yumshoq va qulay tuzilma",
        advantage_3_title_ru="Мягкая и удобная структура",
        advantage_3_title_en="Soft and comfortable texture",
        advantage_3_description_uz="Milliy va zamonaviy dizayn uyg'unligidagi eksklyuziv kolleksiyalar",
        advantage_3_description_ru="Эксклюзивные коллекции в гармонии национального и современного дизайна",
        advantage_3_description_en="Exclusive collections in harmony of national and modern design",
        
        advantage_4_title_uz="Uzoq yillik mustahkamlik",
        advantage_4_title_ru="Долговечность",
        advantage_4_title_en="Long-lasting durability",
        advantage_4_description_uz="Milliy va zamonaviy dizayn uyg'unligidagi eksklyuziv kolleksiyalar",
        advantage_4_description_ru="Эксклюзивные коллекции в гармонии национального и современного дизайна",
        advantage_4_description_en="Exclusive collections in harmony of national and modern design",
        
        # Секция 5: Призыв к действию
        cta_title_uz="Eng yaxshi gilam takliflarini ko'ring",
        cta_title_ru="Посмотрите лучшие предложения ковров",
        cta_title_en="See the best carpet offers",
        cta_description_uz="Uyga iliqlik, qulaylik va stil qo'shadigan eng sifatli gilamlarni bir joyda topladik. Kolleksiyamizni ko'rib, interyeringizga eng mosini tanlang.",
        cta_description_ru="Мы собрали в одном месте самые качественные ковры, которые добавляют тепло, комфорт и стиль в ваш дом. Просмотрите нашу коллекцию и выберите наиболее подходящий для вашего интерьера.",
        cta_description_en="We have gathered the highest quality carpets that add warmth, comfort and style to your home in one place. View our collection and choose the most suitable one for your interior.",
        cta_contact_link="",
        cta_dealer_link="",
        
        is_published=True,
    )


def reverse_create_initial_homepage(apps, schema_editor):
    """Откат создания начальной записи"""
    HomePage = apps.get_model('catalog', 'HomePage')
    HomePage.objects.all().delete()


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0012_maingallery'),
    ]

    operations = [
        # Удаляем старые поля
        migrations.RemoveField(
            model_name='homepage',
            name='image',
        ),
        migrations.RemoveField(
            model_name='homepage',
            name='video',
        ),
        migrations.RemoveField(
            model_name='homepage',
            name='title',
        ),
        migrations.RemoveField(
            model_name='homepage',
            name='title_uz',
        ),
        migrations.RemoveField(
            model_name='homepage',
            name='title_ru',
        ),
        migrations.RemoveField(
            model_name='homepage',
            name='title_en',
        ),
        migrations.RemoveField(
            model_name='homepage',
            name='description',
        ),
        migrations.RemoveField(
            model_name='homepage',
            name='description_uz',
        ),
        migrations.RemoveField(
            model_name='homepage',
            name='description_ru',
        ),
        migrations.RemoveField(
            model_name='homepage',
            name='description_en',
        ),
        migrations.RemoveField(
            model_name='homepage',
            name='collection_link',
        ),
        migrations.RemoveField(
            model_name='homepage',
            name='collection_link_uz',
        ),
        migrations.RemoveField(
            model_name='homepage',
            name='collection_link_ru',
        ),
        migrations.RemoveField(
            model_name='homepage',
            name='collection_link_en',
        ),
        migrations.RemoveField(
            model_name='homepage',
            name='showroom_title',
        ),
        migrations.RemoveField(
            model_name='homepage',
            name='showroom_title_uz',
        ),
        migrations.RemoveField(
            model_name='homepage',
            name='showroom_title_ru',
        ),
        migrations.RemoveField(
            model_name='homepage',
            name='showroom_title_en',
        ),
        migrations.RemoveField(
            model_name='homepage',
            name='showroom_link',
        ),
        migrations.RemoveField(
            model_name='homepage',
            name='showroom_link_uz',
        ),
        migrations.RemoveField(
            model_name='homepage',
            name='showroom_link_ru',
        ),
        migrations.RemoveField(
            model_name='homepage',
            name='showroom_link_en',
        ),
        
        # Добавляем новые поля - Секция 1: Баннер
        migrations.AddField(
            model_name='homepage',
            name='banner_title',
            field=models.CharField(max_length=200, default='', verbose_name='Заголовок баннера'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='homepage',
            name='banner_title_uz',
            field=models.CharField(max_length=200, null=True, verbose_name='Заголовок баннера'),
        ),
        migrations.AddField(
            model_name='homepage',
            name='banner_title_ru',
            field=models.CharField(max_length=200, null=True, verbose_name='Заголовок баннера'),
        ),
        migrations.AddField(
            model_name='homepage',
            name='banner_title_en',
            field=models.CharField(max_length=200, null=True, verbose_name='Заголовок баннера'),
        ),
        migrations.AddField(
            model_name='homepage',
            name='banner_description',
            field=models.TextField(default='', verbose_name='Описание баннера'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='homepage',
            name='banner_description_uz',
            field=models.TextField(null=True, verbose_name='Описание баннера'),
        ),
        migrations.AddField(
            model_name='homepage',
            name='banner_description_ru',
            field=models.TextField(null=True, verbose_name='Описание баннера'),
        ),
        migrations.AddField(
            model_name='homepage',
            name='banner_description_en',
            field=models.TextField(null=True, verbose_name='Описание баннера'),
        ),
        migrations.AddField(
            model_name='homepage',
            name='banner_link',
            field=models.CharField(blank=True, max_length=500, verbose_name='Ссылка баннера'),
        ),
        migrations.AddField(
            model_name='homepage',
            name='banner_link_uz',
            field=models.CharField(blank=True, max_length=500, null=True, verbose_name='Ссылка баннера'),
        ),
        migrations.AddField(
            model_name='homepage',
            name='banner_link_ru',
            field=models.CharField(blank=True, max_length=500, null=True, verbose_name='Ссылка баннера'),
        ),
        migrations.AddField(
            model_name='homepage',
            name='banner_link_en',
            field=models.CharField(blank=True, max_length=500, null=True, verbose_name='Ссылка баннера'),
        ),
        migrations.AddField(
            model_name='homepage',
            name='banner_image',
            field=models.ImageField(blank=True, null=True, upload_to='photos/homepage/banner/%Y/%m/', verbose_name='Изображение баннера'),
        ),
        migrations.AddField(
            model_name='homepage',
            name='banner_video',
            field=models.FileField(blank=True, null=True, upload_to='files/homepage/banner/%Y/%m/', verbose_name='Видео баннера'),
        ),
        migrations.AddField(
            model_name='homepage',
            name='banner_showroom_title',
            field=models.CharField(default='', max_length=200, verbose_name='Заголовок шоурума'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='homepage',
            name='banner_showroom_title_uz',
            field=models.CharField(max_length=200, null=True, verbose_name='Заголовок шоурума'),
        ),
        migrations.AddField(
            model_name='homepage',
            name='banner_showroom_title_ru',
            field=models.CharField(max_length=200, null=True, verbose_name='Заголовок шоурума'),
        ),
        migrations.AddField(
            model_name='homepage',
            name='banner_showroom_title_en',
            field=models.CharField(max_length=200, null=True, verbose_name='Заголовок шоурума'),
        ),
        migrations.AddField(
            model_name='homepage',
            name='banner_showroom_link',
            field=models.CharField(blank=True, max_length=500, verbose_name='Ссылка шоурума'),
        ),
        migrations.AddField(
            model_name='homepage',
            name='banner_showroom_link_uz',
            field=models.CharField(blank=True, max_length=500, null=True, verbose_name='Ссылка шоурума'),
        ),
        migrations.AddField(
            model_name='homepage',
            name='banner_showroom_link_ru',
            field=models.CharField(blank=True, max_length=500, null=True, verbose_name='Ссылка шоурума'),
        ),
        migrations.AddField(
            model_name='homepage',
            name='banner_showroom_link_en',
            field=models.CharField(blank=True, max_length=500, null=True, verbose_name='Ссылка шоурума'),
        ),
        migrations.AddField(
            model_name='homepage',
            name='banner_showroom_image',
            field=models.ImageField(blank=True, null=True, upload_to='photos/homepage/showroom/%Y/%m/', verbose_name='Изображение шоурума'),
        ),
        
        # Добавляем новые поля - Секция 2: О нас
        migrations.AddField(
            model_name='homepage',
            name='about_title',
            field=models.CharField(default='', max_length=200, verbose_name='Заголовок секции "О нас"'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='homepage',
            name='about_title_uz',
            field=models.CharField(max_length=200, null=True, verbose_name='Заголовок секции "О нас"'),
        ),
        migrations.AddField(
            model_name='homepage',
            name='about_title_ru',
            field=models.CharField(max_length=200, null=True, verbose_name='Заголовок секции "О нас"'),
        ),
        migrations.AddField(
            model_name='homepage',
            name='about_title_en',
            field=models.CharField(max_length=200, null=True, verbose_name='Заголовок секции "О нас"'),
        ),
        migrations.AddField(
            model_name='homepage',
            name='about_link',
            field=models.CharField(blank=True, max_length=500, verbose_name='Ссылка секции "О нас"'),
        ),
        migrations.AddField(
            model_name='homepage',
            name='about_link_uz',
            field=models.CharField(blank=True, max_length=500, null=True, verbose_name='Ссылка секции "О нас"'),
        ),
        migrations.AddField(
            model_name='homepage',
            name='about_link_ru',
            field=models.CharField(blank=True, max_length=500, null=True, verbose_name='Ссылка секции "О нас"'),
        ),
        migrations.AddField(
            model_name='homepage',
            name='about_link_en',
            field=models.CharField(blank=True, max_length=500, null=True, verbose_name='Ссылка секции "О нас"'),
        ),
        migrations.AddField(
            model_name='homepage',
            name='about_youtube_link',
            field=models.CharField(blank=True, max_length=500, verbose_name='Ссылка на YouTube'),
        ),
        migrations.AddField(
            model_name='homepage',
            name='about_youtube_link_uz',
            field=models.CharField(blank=True, max_length=500, null=True, verbose_name='Ссылка на YouTube'),
        ),
        migrations.AddField(
            model_name='homepage',
            name='about_youtube_link_ru',
            field=models.CharField(blank=True, max_length=500, null=True, verbose_name='Ссылка на YouTube'),
        ),
        migrations.AddField(
            model_name='homepage',
            name='about_youtube_link_en',
            field=models.CharField(blank=True, max_length=500, null=True, verbose_name='Ссылка на YouTube'),
        ),
        migrations.AddField(
            model_name='homepage',
            name='about_bottom_description',
            field=models.TextField(default='', verbose_name='Нижнее описание секции "О нас"'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='homepage',
            name='about_bottom_description_uz',
            field=models.TextField(null=True, verbose_name='Нижнее описание секции "О нас"'),
        ),
        migrations.AddField(
            model_name='homepage',
            name='about_bottom_description_ru',
            field=models.TextField(null=True, verbose_name='Нижнее описание секции "О нас"'),
        ),
        migrations.AddField(
            model_name='homepage',
            name='about_bottom_description_en',
            field=models.TextField(null=True, verbose_name='Нижнее описание секции "О нас"'),
        ),
        migrations.AddField(
            model_name='homepage',
            name='about_image_1',
            field=models.ImageField(blank=True, null=True, upload_to='photos/homepage/about/%Y/%m/', verbose_name='Изображение 1 (обязательное)'),
        ),
        migrations.AddField(
            model_name='homepage',
            name='about_image_2',
            field=models.ImageField(blank=True, null=True, upload_to='photos/homepage/about/%Y/%m/', verbose_name='Изображение 2'),
        ),
        migrations.AddField(
            model_name='homepage',
            name='about_image_3',
            field=models.ImageField(blank=True, null=True, upload_to='photos/homepage/about/%Y/%m/', verbose_name='Изображение 3'),
        ),
        
        # Добавляем новые поля - Секция 3: Шоурум
        migrations.AddField(
            model_name='homepage',
            name='showroom_image',
            field=models.ImageField(blank=True, null=True, upload_to='photos/homepage/showroom_section/%Y/%m/', verbose_name='Изображение секции шоурума'),
        ),
        migrations.AddField(
            model_name='homepage',
            name='showroom_title',
            field=models.CharField(default='', max_length=200, verbose_name='Заголовок секции шоурума'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='homepage',
            name='showroom_title_uz',
            field=models.CharField(max_length=200, null=True, verbose_name='Заголовок секции шоурума'),
        ),
        migrations.AddField(
            model_name='homepage',
            name='showroom_title_ru',
            field=models.CharField(max_length=200, null=True, verbose_name='Заголовок секции шоурума'),
        ),
        migrations.AddField(
            model_name='homepage',
            name='showroom_title_en',
            field=models.CharField(max_length=200, null=True, verbose_name='Заголовок секции шоурума'),
        ),
        migrations.AddField(
            model_name='homepage',
            name='showroom_link',
            field=models.CharField(blank=True, max_length=500, verbose_name='Ссылка секции шоурума'),
        ),
        migrations.AddField(
            model_name='homepage',
            name='showroom_link_uz',
            field=models.CharField(blank=True, max_length=500, null=True, verbose_name='Ссылка секции шоурума'),
        ),
        migrations.AddField(
            model_name='homepage',
            name='showroom_link_ru',
            field=models.CharField(blank=True, max_length=500, null=True, verbose_name='Ссылка секции шоурума'),
        ),
        migrations.AddField(
            model_name='homepage',
            name='showroom_link_en',
            field=models.CharField(blank=True, max_length=500, null=True, verbose_name='Ссылка секции шоурума'),
        ),
        
        # Добавляем новые поля - Секция 4: Преимущества
        migrations.AddField(
            model_name='homepage',
            name='advantage_1_title',
            field=models.CharField(default='', max_length=200, verbose_name='Заголовок карточки 1'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='homepage',
            name='advantage_1_title_uz',
            field=models.CharField(max_length=200, null=True, verbose_name='Заголовок карточки 1'),
        ),
        migrations.AddField(
            model_name='homepage',
            name='advantage_1_title_ru',
            field=models.CharField(max_length=200, null=True, verbose_name='Заголовок карточки 1'),
        ),
        migrations.AddField(
            model_name='homepage',
            name='advantage_1_title_en',
            field=models.CharField(max_length=200, null=True, verbose_name='Заголовок карточки 1'),
        ),
        migrations.AddField(
            model_name='homepage',
            name='advantage_1_icon',
            field=models.FileField(blank=True, null=True, upload_to='icons/homepage/%Y/%m/', verbose_name='SVG иконка карточки 1'),
        ),
        migrations.AddField(
            model_name='homepage',
            name='advantage_1_description',
            field=models.TextField(default='', verbose_name='Описание карточки 1'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='homepage',
            name='advantage_1_description_uz',
            field=models.TextField(null=True, verbose_name='Описание карточки 1'),
        ),
        migrations.AddField(
            model_name='homepage',
            name='advantage_1_description_ru',
            field=models.TextField(null=True, verbose_name='Описание карточки 1'),
        ),
        migrations.AddField(
            model_name='homepage',
            name='advantage_1_description_en',
            field=models.TextField(null=True, verbose_name='Описание карточки 1'),
        ),
        migrations.AddField(
            model_name='homepage',
            name='advantage_2_title',
            field=models.CharField(default='', max_length=200, verbose_name='Заголовок карточки 2'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='homepage',
            name='advantage_2_title_uz',
            field=models.CharField(max_length=200, null=True, verbose_name='Заголовок карточки 2'),
        ),
        migrations.AddField(
            model_name='homepage',
            name='advantage_2_title_ru',
            field=models.CharField(max_length=200, null=True, verbose_name='Заголовок карточки 2'),
        ),
        migrations.AddField(
            model_name='homepage',
            name='advantage_2_title_en',
            field=models.CharField(max_length=200, null=True, verbose_name='Заголовок карточки 2'),
        ),
        migrations.AddField(
            model_name='homepage',
            name='advantage_2_description',
            field=models.TextField(default='', verbose_name='Описание карточки 2'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='homepage',
            name='advantage_2_description_uz',
            field=models.TextField(null=True, verbose_name='Описание карточки 2'),
        ),
        migrations.AddField(
            model_name='homepage',
            name='advantage_2_description_ru',
            field=models.TextField(null=True, verbose_name='Описание карточки 2'),
        ),
        migrations.AddField(
            model_name='homepage',
            name='advantage_2_description_en',
            field=models.TextField(null=True, verbose_name='Описание карточки 2'),
        ),
        migrations.AddField(
            model_name='homepage',
            name='advantage_3_title',
            field=models.CharField(default='', max_length=200, verbose_name='Заголовок карточки 3'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='homepage',
            name='advantage_3_title_uz',
            field=models.CharField(max_length=200, null=True, verbose_name='Заголовок карточки 3'),
        ),
        migrations.AddField(
            model_name='homepage',
            name='advantage_3_title_ru',
            field=models.CharField(max_length=200, null=True, verbose_name='Заголовок карточки 3'),
        ),
        migrations.AddField(
            model_name='homepage',
            name='advantage_3_title_en',
            field=models.CharField(max_length=200, null=True, verbose_name='Заголовок карточки 3'),
        ),
        migrations.AddField(
            model_name='homepage',
            name='advantage_3_description',
            field=models.TextField(default='', verbose_name='Описание карточки 3'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='homepage',
            name='advantage_3_description_uz',
            field=models.TextField(null=True, verbose_name='Описание карточки 3'),
        ),
        migrations.AddField(
            model_name='homepage',
            name='advantage_3_description_ru',
            field=models.TextField(null=True, verbose_name='Описание карточки 3'),
        ),
        migrations.AddField(
            model_name='homepage',
            name='advantage_3_description_en',
            field=models.TextField(null=True, verbose_name='Описание карточки 3'),
        ),
        migrations.AddField(
            model_name='homepage',
            name='advantage_4_title',
            field=models.CharField(default='', max_length=200, verbose_name='Заголовок карточки 4'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='homepage',
            name='advantage_4_title_uz',
            field=models.CharField(max_length=200, null=True, verbose_name='Заголовок карточки 4'),
        ),
        migrations.AddField(
            model_name='homepage',
            name='advantage_4_title_ru',
            field=models.CharField(max_length=200, null=True, verbose_name='Заголовок карточки 4'),
        ),
        migrations.AddField(
            model_name='homepage',
            name='advantage_4_title_en',
            field=models.CharField(max_length=200, null=True, verbose_name='Заголовок карточки 4'),
        ),
        migrations.AddField(
            model_name='homepage',
            name='advantage_4_icon',
            field=models.FileField(blank=True, null=True, upload_to='icons/homepage/%Y/%m/', verbose_name='SVG иконка карточки 4'),
        ),
        migrations.AddField(
            model_name='homepage',
            name='advantage_4_description',
            field=models.TextField(default='', verbose_name='Описание карточки 4'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='homepage',
            name='advantage_4_description_uz',
            field=models.TextField(null=True, verbose_name='Описание карточки 4'),
        ),
        migrations.AddField(
            model_name='homepage',
            name='advantage_4_description_ru',
            field=models.TextField(null=True, verbose_name='Описание карточки 4'),
        ),
        migrations.AddField(
            model_name='homepage',
            name='advantage_4_description_en',
            field=models.TextField(null=True, verbose_name='Описание карточки 4'),
        ),
        
        # Добавляем новые поля - Секция 5: Призыв к действию
        migrations.AddField(
            model_name='homepage',
            name='cta_title',
            field=models.CharField(default='', max_length=200, verbose_name='Заголовок призыва к действию'),
            preserve_default=False,
        ),
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
            name='cta_description',
            field=models.TextField(default='', verbose_name='Описание призыва к действию'),
            preserve_default=False,
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
        migrations.AddField(
            model_name='homepage',
            name='cta_contact_link',
            field=models.CharField(blank=True, max_length=500, verbose_name='Ссылка на форму для связи'),
        ),
        migrations.AddField(
            model_name='homepage',
            name='cta_dealer_link',
            field=models.CharField(blank=True, max_length=500, verbose_name='Ссылка на форму для становления дилера'),
        ),
        
        # Обновляем опции модели
        migrations.AlterModelOptions(
            name='homepage',
            options={'ordering': ['-created_at'], 'verbose_name': 'Главная страница', 'verbose_name_plural': 'Главная страница'},
        ),
        
        # Создаем начальную запись
        migrations.RunPython(create_initial_homepage, reverse_create_initial_homepage),
    ]
