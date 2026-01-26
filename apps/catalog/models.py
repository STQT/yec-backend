from django.db import models
from django.urls import reverse
import os


# Модель для этапов производства
class ProductionStep(models.Model):
    """Этап производства"""
    about_page = models.ForeignKey(
        'AboutPage',
        on_delete=models.CASCADE,
        related_name='production_steps',
        verbose_name='Страница о компании'
    )
    title = models.CharField(max_length=200, verbose_name='Заголовок этапа')
    description = models.TextField(verbose_name='Описание этапа')
    image = models.ImageField(
        upload_to='photos/production_steps/%Y/%m/',
        verbose_name='Изображение этапа',
        blank=True,
        null=True
    )
    order = models.PositiveIntegerField(default=0, verbose_name='Порядок сортировки')
    
    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name = 'Этап производства'
        verbose_name_plural = 'Этапы производства'
        ordering = ['order']


# Модель для истории компании
class CompanyHistory(models.Model):
    """История компании"""
    about_page = models.ForeignKey(
        'AboutPage',
        on_delete=models.CASCADE,
        related_name='company_history',
        verbose_name='Страница о компании'
    )
    year = models.PositiveIntegerField(verbose_name='Год')
    title = models.CharField(max_length=200, verbose_name='Заголовок события')
    description = models.TextField(verbose_name='Описание события')
    image = models.ImageField(
        upload_to='photos/company_history/%Y/%m/',
        verbose_name='Изображение события',
        blank=True,
        null=True
    )
    order = models.PositiveIntegerField(default=0, verbose_name='Порядок сортировки')
    
    def __str__(self):
        return f"{self.year} - {self.title}"
    
    class Meta:
        verbose_name = 'История компании'
        verbose_name_plural = 'История компании'
        ordering = ['order', 'year']


# Модель для объемов производства
class ProductionCapacity(models.Model):
    """Объем производства"""
    about_page = models.ForeignKey(
        'AboutPage',
        on_delete=models.CASCADE,
        related_name='production_capacity',
        verbose_name='Страница о компании'
    )
    year = models.PositiveIntegerField(verbose_name='Год')
    capacity = models.CharField(max_length=100, verbose_name='Объем производства')
    description = models.TextField(verbose_name='Описание', blank=True)
    image = models.ImageField(
        upload_to='photos/production_capacity/%Y/%m/',
        verbose_name='Изображение',
        blank=True,
        null=True
    )
    order = models.PositiveIntegerField(default=0, verbose_name='Порядок сортировки')
    
    def __str__(self):
        return f"{self.year} - {self.capacity}"
    
    class Meta:
        verbose_name = 'Объем производства'
        verbose_name_plural = 'Объемы производства'
        ordering = ['order', 'year']


# Модель Collection
class Collection(models.Model):
    name = models.CharField(max_length=50, verbose_name='Категория')
    description = models.TextField(default='Описания коллекции', verbose_name='Описания', blank=True, null=True)
    image = models.ImageField(upload_to='photos/collection_avatar/%Y/%m/', verbose_name='photo Коллекции')
    is_published = models.BooleanField(default=True, verbose_name='Публикация')
    slug = models.SlugField(unique=True, null=True, verbose_name='Slug')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    update_at = models.DateTimeField(auto_now=True, verbose_name='Дата обновления')
    is_new = models.BooleanField(default=False, verbose_name='Новая коллекция')

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('catalog:collection', kwargs={'collection_slug': self.slug})

    class Meta:
        verbose_name = 'Коллекция'
        verbose_name_plural = 'Коллекции'


# Функция для определения пути загрузки изображений
def carpet_image_upload_to(instance, filename):
    # Получаем имя коллекции
    collection_name = instance.collection.name
    # Формируем путь к файлу
    return os.path.join('photos/collections', collection_name, filename)


# Модель для стилей ковров
class Style(models.Model):
    name = models.CharField(max_length=50, verbose_name='Название стиля')
    slug = models.SlugField(unique=True, verbose_name='Slug')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Стиль'
        verbose_name_plural = 'Стили'


# Модель для комнат
class Room(models.Model):
    name = models.CharField(max_length=50, verbose_name='Название комнаты')
    slug = models.SlugField(unique=True, verbose_name='Slug')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Комната'
        verbose_name_plural = 'Комнаты'


# Модель для цветов
class Color(models.Model):
    name = models.CharField(max_length=50, verbose_name='Название цвета')
    slug = models.SlugField(unique=True, verbose_name='Slug')
    hex_code = models.CharField(max_length=7, blank=True, null=True, verbose_name='HEX код цвета',
                                help_text='Например: #FF5733')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Цвет'
        verbose_name_plural = 'Цвета'


# Модель Carpet с дополнениями из Figma
class Carpet(models.Model):
    code = models.CharField(max_length=32, verbose_name='Код Ковра', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    update_at = models.DateTimeField(auto_now=True, verbose_name='Дата обновления')
    photo = models.ImageField(upload_to=carpet_image_upload_to, blank=True, null=True, verbose_name='Изображения')
    watched = models.IntegerField(default=0, verbose_name='Просмотры')
    is_published = models.BooleanField(default=True, verbose_name='Публикация')
    collection = models.ForeignKey(Collection, on_delete=models.CASCADE, verbose_name='Коллекция',
                                   related_name='carpets')
    roll = models.BooleanField(default=False, verbose_name='Рулон')
    
    # Новые поля из Figma
    material = models.CharField(max_length=200, blank=True, null=True, verbose_name='Материал',
                                help_text='Например: jun va ipak (шерсть и шелк)')
    density = models.CharField(max_length=100, blank=True, null=True, verbose_name='Плотность',
                               help_text='Например: 1 m² ga 2880000 tugun')
    base = models.CharField(max_length=100, blank=True, null=True, verbose_name='Основа',
                            help_text='Например: paxta (хлопок)')
    pile_height = models.CharField(max_length=20, blank=True, null=True, verbose_name='Высота ворса',
                                   help_text='Например: 5mm')
    yarn_composition = models.CharField(max_length=100, blank=True, null=True, verbose_name='Состав нити',
                                        help_text='Например: 100%modal')
    weight = models.CharField(max_length=100, blank=True, null=True, verbose_name='Вес',
                              help_text='Например: 2850 gr/m² (+/-7%)')
    
    # Флаги для фильтрации
    is_new = models.BooleanField(default=False, verbose_name='Новый')
    is_popular = models.BooleanField(default=False, verbose_name='Популярный')
    
    # Связи для фильтрации
    styles = models.ManyToManyField(Style, blank=True, verbose_name='Стили', related_name='carpets')
    rooms = models.ManyToManyField(Room, blank=True, verbose_name='Комнаты', related_name='carpets')
    colors = models.ManyToManyField(Color, blank=True, verbose_name='Цвета', related_name='carpets')

    def save(self, *args, **kwargs):
        # Если имя товара не задано, берем его из имени файла изображения
        if not self.code and self.photo:
            # Извлекаем имя файла без расширения
            self.code = self.photo.name.split('/')[-1].split('.')[0]
        super(Carpet, self).save(*args, **kwargs)

    def __str__(self):
        return self.code or f'Ковер #{self.id}'

    class Meta:
        verbose_name = 'Ковер'
        verbose_name_plural = 'Ковры'
        ordering = ['-created_at']


# Модель для новостей
class News(models.Model):
    title = models.CharField(max_length=200, verbose_name='Заголовок')
    slug = models.SlugField(unique=True, verbose_name='Slug')
    description = models.TextField(blank=True, null=True, verbose_name='Краткое описание')
    cover_image = models.ImageField(
        upload_to='photos/news/%Y/%m/', 
        verbose_name='Главное изображение', 
        blank=True, 
        null=True,
        help_text='Изображение для превью новости'
    )
    is_published = models.BooleanField(default=True, verbose_name='Публикация')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    update_at = models.DateTimeField(auto_now=True, verbose_name='Дата обновления')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Новость'
        verbose_name_plural = 'Новости'
        ordering = ['-created_at']

    def get_absolute_url(self):
        return reverse('catalog:news_detail', kwargs={'news_slug': self.slug})


class NewsContentBlock(models.Model):
    """Блок контента новости (текст или изображения)"""
    CONTENT_TYPE_CHOICES = [
        ('text', 'Текстовый блок'),
        ('images', 'Блок изображений'),
    ]
    
    news = models.ForeignKey(
        News,
        on_delete=models.CASCADE,
        related_name='content_blocks',
        verbose_name='Новость'
    )
    content_type = models.CharField(
        max_length=10,
        choices=CONTENT_TYPE_CHOICES,
        default='text',
        verbose_name='Тип блока'
    )
    title = models.CharField(
        max_length=200,
        blank=True,
        verbose_name='Заголовок блока',
        help_text='Опциональный заголовок для блока контента'
    )
    text_content = models.TextField(
        blank=True,
        null=True,
        verbose_name='Текстовое содержание',
        help_text='Используется для текстовых блоков. Поддерживает HTML (CKEditor)'
    )
    order = models.PositiveIntegerField(default=0, verbose_name='Порядок')
    
    def __str__(self):
        return f"{self.news.title} - {self.get_content_type_display()} #{self.order}"
    
    class Meta:
        verbose_name = 'Блок контента новости'
        verbose_name_plural = 'Блоки контента новости'
        ordering = ['order']


class NewsImage(models.Model):
    """Изображение для блока изображений новости"""
    content_block = models.ForeignKey(
        NewsContentBlock,
        on_delete=models.CASCADE,
        related_name='images',
        verbose_name='Блок контента',
        limit_choices_to={'content_type': 'images'}
    )
    image = models.ImageField(
        upload_to='photos/news/content/%Y/%m/',
        verbose_name='Изображение'
    )
    caption = models.CharField(
        max_length=200,
        blank=True,
        null=True,
        verbose_name='Подпись к изображению'
    )
    order = models.PositiveIntegerField(default=0, verbose_name='Порядок')
    
    def __str__(self):
        return f"Image {self.order} - {self.content_block.news.title}"
    
    class Meta:
        verbose_name = 'Изображение новости'
        verbose_name_plural = 'Изображения новости'
        ordering = ['order']


# Модель для галереи
class Gallery(models.Model):
    title = models.CharField(max_length=200, blank=True, null=True, verbose_name='Название')
    image = models.ImageField(upload_to='photos/gallery/%Y/%m/', verbose_name='Изображение')
    is_published = models.BooleanField(default=True, verbose_name='Публикация')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    order = models.PositiveIntegerField(default=0, verbose_name='Порядок сортировки')

    def __str__(self):
        return self.title or f'Изображение #{self.id}'

    class Meta:
        verbose_name = 'Изображение галереи'
        verbose_name_plural = 'Галерея'
        ordering = ['order', '-created_at']


# Модель для главной страницы
class HomePage(models.Model):
    """Модель главной страницы с мультиязычными полями"""
    image = models.ImageField(upload_to='photos/homepage/%Y/%m/', verbose_name='Изображение')
    video = models.FileField(upload_to='files/homepage/%Y/%m/', verbose_name='Видео')
    
    # Мультиязычные поля
    title = models.CharField(max_length=200, verbose_name='Заголовок')
    description = models.TextField(verbose_name='Описание')
    collection_link = models.CharField(max_length=200, verbose_name='Ссылка на коллекцию')
    
    # Поля для шоурума
    showroom_title = models.CharField(max_length=200, verbose_name='Заголовок шоурума')
    showroom_link = models.CharField(max_length=200, verbose_name='Ссылка на шоурум')
    
    is_published = models.BooleanField(default=True, verbose_name='Публикация')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    update_at = models.DateTimeField(auto_now=True, verbose_name='Дата обновления')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Главная секция'
        verbose_name_plural = 'Главная секция'
        ordering = ['-created_at']


# Модель для страницы "О компании"

class AboutPage(models.Model):
    """Модель страницы о компании - все данные в одной модели"""
    
    # Основная информация о компании
    company_title = models.CharField(max_length=200, verbose_name='Название компании')
    company_subtitle = models.CharField(max_length=200, blank=True, null=True, verbose_name='Подзаголовок')
    company_description = models.TextField(verbose_name='Описание компании')
    main_image = models.ImageField(upload_to='photos/about/%Y/%m/', verbose_name='Главное изображение')
    showroom_image = models.ImageField(upload_to='photos/about/showroom/%Y/%m/', verbose_name='Изображение шоурума')
    
    # Заголовки секций
    production_section_title = models.CharField(
        max_length=200, 
        default='Ishlab chiqarish jarayoni', 
        verbose_name='Заголовок секции производства'
    )
    history_section_title = models.CharField(
        max_length=200, 
        default='Kompaniya tarixi',
        verbose_name='Заголовок секции истории'
    )
    capacity_section_title = models.CharField(
        max_length=200, 
        default='Ishlab chiqarish hajmi',
        verbose_name='Заголовок секции объемов'
    )
    dealer_section_title = models.CharField(
        max_length=200, 
        default='Dilerlar uchun hamkorlik',
        verbose_name='Заголовок секции для дилеров'
    )
    showroom_button_text = models.CharField(
        max_length=100, 
        default="To'liq ekranda ko'rish",
        verbose_name='Текст кнопки шоурума'
    )
    
    is_published = models.BooleanField(default=True, verbose_name='Публикация')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    update_at = models.DateTimeField(auto_now=True, verbose_name='Дата обновления')

    def __str__(self):
        return self.company_title

    class Meta:
        verbose_name = 'Страница о компании'
        verbose_name_plural = 'Страница о компании'
        ordering = ['-created_at']


class DealerAdvantage(models.Model):
    """Модель преимуществ для дилеров"""
    about_page = models.ForeignKey(
        AboutPage,
        on_delete=models.CASCADE,
        related_name='dealer_advantages',
        verbose_name='Страница о компании'
    )
    title = models.CharField(max_length=200, verbose_name='Заголовок')
    description = models.TextField(verbose_name='Описание')
    order = models.PositiveIntegerField(default=0, verbose_name='Порядок сортировки')
    is_published = models.BooleanField(default=True, verbose_name='Публикация')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Преимущество для дилеров'
        verbose_name_plural = 'Преимущества для дилеров'
        ordering = ['order']


# Модели для страницы контактов

class ContactPage(models.Model):
    """Модель страницы контактов"""
    # Основная информация
    page_title = models.CharField(max_length=200, default='Bizning kontaktlarimiz', verbose_name='Заголовок страницы')
    
    # Адрес
    address_label = models.CharField(max_length=100, default='Manzil', verbose_name='Метка адреса')
    address = models.TextField(verbose_name='Адрес')
    
    # Телефон
    phone_label = models.CharField(max_length=100, default='Telefon raqam', verbose_name='Метка телефона')
    phone = models.CharField(max_length=50, verbose_name='Телефон')
    
    # Email
    email_label = models.CharField(max_length=100, default='Elektron pochta', verbose_name='Метка email')
    email = models.EmailField(verbose_name='Email')
    
    # Карта
    map_embed_url = models.URLField(
        blank=True, 
        null=True, 
        verbose_name='Ссылка на Google Maps',
        help_text='Например: https://maps.google.com/...'
    )
    
    # Форма обратной связи
    form_title = models.CharField(max_length=200, default='Shaxsiy maslahat oling', verbose_name='Заголовок формы')
    form_description = models.TextField(
        default='Gilam tanlashda yordam kerakmi? Kontaktlaringizni qoldiring...',
        verbose_name='Описание формы'
    )
    
    # Социальные сети
    facebook_url = models.URLField(blank=True, null=True, verbose_name='Facebook')
    twitter_url = models.URLField(blank=True, null=True, verbose_name='Twitter')
    linkedin_url = models.URLField(blank=True, null=True, verbose_name='LinkedIn')
    instagram_url = models.URLField(blank=True, null=True, verbose_name='Instagram')
    
    is_published = models.BooleanField(default=True, verbose_name='Публикация')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    update_at = models.DateTimeField(auto_now=True, verbose_name='Дата обновления')
    
    def __str__(self):
        return self.page_title
    
    class Meta:
        verbose_name = 'Страница контактов'
        verbose_name_plural = 'Страница контактов'


# Модели для торговых точек

class Region(models.Model):
    """Модель региона (области)"""
    name = models.CharField(max_length=200, verbose_name='Название региона')
    slug = models.SlugField(unique=True, verbose_name='Slug')
    order = models.PositiveIntegerField(default=0, verbose_name='Порядок сортировки')
    is_published = models.BooleanField(default=True, verbose_name='Публикация')
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = 'Регион'
        verbose_name_plural = 'Регионы'
        ordering = ['order', 'name']


class PointType(models.Model):
    """Модель типа торговой точки"""
    name = models.CharField(max_length=200, verbose_name='Название типа')
    slug = models.SlugField(unique=True, verbose_name='Slug')
    order = models.PositiveIntegerField(default=0, verbose_name='Порядок сортировки')
    is_published = models.BooleanField(default=True, verbose_name='Публикация')
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = 'Тип точки'
        verbose_name_plural = 'Типы точек'
        ordering = ['order', 'name']


class SalesPoint(models.Model):
    """Модель торговой точки"""
    region = models.ForeignKey(
        Region,
        on_delete=models.CASCADE,
        related_name='sales_points',
        verbose_name='Регион'
    )
    
    # Основная информация
    name = models.CharField(max_length=200, verbose_name='Название точки')
    point_type = models.ForeignKey(
        PointType,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='sales_points',
        verbose_name='Тип точки'
    )
    
    # Адрес
    address = models.TextField(verbose_name='Адрес')
    location = models.CharField(
        max_length=200,
        blank=True,
        null=True,
        verbose_name='Местоположение',
        help_text='Например: Farhod qo\'rg\'oni 25-A'
    )
    
    # Контакты
    phone = models.CharField(max_length=50, verbose_name='Телефон')
    
    # Ссылка на карту
    map_link = models.URLField(
        max_length=500,
        blank=True,
        null=True,
        verbose_name='Ссылка на карту',
        help_text='Ссылка на Google Maps или Яндекс.Карты'
    )
    
    # Дополнительно
    order = models.PositiveIntegerField(default=0, verbose_name='Порядок сортировки')
    is_published = models.BooleanField(default=True, verbose_name='Публикация')
    
    def __str__(self):
        return f"{self.name} - {self.region.name}"
    
    class Meta:
        verbose_name = 'Торговая точка'
        verbose_name_plural = 'Торговые точки'
        ordering = ['region__order', 'order', 'name']


# Модель для формы заявки

class ContactFormSubmission(models.Model):
    """Модель заявки из формы обратной связи"""
    STATUS_CHOICES = [
        ('new', 'Новая'),
        ('in_progress', 'В обработке'),
        ('completed', 'Завершена'),
        ('cancelled', 'Отменена'),
    ]
    
    name = models.CharField(max_length=200, verbose_name='Имя')
    phone = models.CharField(max_length=50, verbose_name='Телефон')
    email = models.EmailField(verbose_name='Email', blank=True, null=True)
    message = models.TextField(verbose_name='Сообщение', blank=True, null=True)
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='new',
        verbose_name='Статус'
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата обновления')
    notes = models.TextField(blank=True, null=True, verbose_name='Примечания администратора')
    
    def __str__(self):
        return f"{self.name} - {self.phone} ({self.created_at.strftime('%d.%m.%Y')})"
    
    class Meta:
        verbose_name = 'Заявка'
        verbose_name_plural = 'Заявки'
        ordering = ['-created_at']


# Модель для FAQ

class FAQ(models.Model):
    """Модель вопросов и ответов"""
    question = models.TextField(verbose_name='Вопрос')
    answer = models.TextField(verbose_name='Ответ')
    order = models.PositiveIntegerField(default=0, verbose_name='Порядок сортировки')
    is_published = models.BooleanField(default=True, verbose_name='Публикация')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    
    def __str__(self):
        return self.question[:100]
    
    class Meta:
        verbose_name = 'Вопрос-Ответ (FAQ)'
        verbose_name_plural = 'Вопросы-Ответы (FAQ)'
        ordering = ['order']


# Модель для карточек преимуществ на главной странице

class AdvantageCard(models.Model):
    """Модель карточки преимуществ для главной страницы"""
    title = models.CharField(max_length=200, verbose_name='Заголовок')
    description = models.TextField(verbose_name='Описание')
    svg_icon = models.TextField(
        blank=True,
        null=True,
        verbose_name='SVG иконка',
        help_text='Вставьте код SVG иконки'
    )
    order = models.PositiveIntegerField(default=0, verbose_name='Порядок (1-4)')
    is_published = models.BooleanField(default=True, verbose_name='Публикация')
    
    def __str__(self):
        return f"Карточка {self.order}: {self.title}"
    
    class Meta:
        verbose_name = 'Карточка преимущества'
        verbose_name_plural = 'Карточки преимуществ'
        ordering = ['order']
