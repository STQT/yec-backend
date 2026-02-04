from django.core.exceptions import ValidationError
from django.db import models
from django.urls import reverse
from django.utils.text import slugify
import os
import re
import random


def generate_unique_slug(model_class, source_text, current_pk=None, current_slug=None):
    """
    Универсальная функция для генерации уникального slug
    
    Args:
        model_class: Класс модели
        source_text: Текст для генерации slug
        current_pk: PK текущего объекта (для исключения из проверки уникальности)
        current_slug: Текущий slug (для проверки, нужно ли обновлять)
    
    Returns:
        str: Уникальный slug
    """
    if not source_text:
        return None
    
    # Преобразуем в строку и очищаем
    source_text = str(source_text).strip()
    if not source_text:
        return None
    
    new_slug = slugify(source_text)
    
    # Если slugify вернул пустую строку (например, только числа или спецсимволы),
    # создаем slug из исходного текста с заменой недопустимых символов
    if not new_slug:
        # Заменяем все недопустимые символы на дефисы и удаляем лишние
        new_slug = re.sub(r'[^\w\s-]', '', source_text)
        new_slug = re.sub(r'[-\s]+', '-', new_slug)
        new_slug = new_slug.strip('-').lower()
        
        # Если все еще пусто, используем fallback
        if not new_slug:
            # Используем префикс модели и текущий PK или случайное число
            model_name = model_class.__name__.lower()
            if current_pk:
                new_slug = f"{model_name}-{current_pk}"
            else:
                new_slug = f"{model_name}-{random.randint(10000, 99999)}"
    
    # Проверяем уникальность и добавляем число если нужно
    original_slug = new_slug
    counter = 1
    queryset = model_class.objects.filter(slug=new_slug)
    if current_pk:
        queryset = queryset.exclude(pk=current_pk)
    
    while queryset.exists():
        new_slug = f"{original_slug}-{counter}"
        queryset = model_class.objects.filter(slug=new_slug)
        if current_pk:
            queryset = queryset.exclude(pk=current_pk)
        counter += 1
        # Защита от бесконечного цикла
        if counter > 1000:
            break
    
    return new_slug


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
    year_title = models.CharField(max_length=200, blank=True, null=True, verbose_name='Название года')
    year_description = models.TextField(blank=True, null=True, verbose_name='Описание года')
    image = models.ImageField(
        upload_to='photos/company_history/%Y/%m/',
        blank=True,
        null=True,
        verbose_name='Изображение'
    )
    
    def __str__(self):
        return f"{self.year} - {self.year_title}"
    
    class Meta:
        verbose_name = 'История компании'
        verbose_name_plural = 'История компании'
        ordering = ['year']


# Модель ProductionCapacity удалена - теперь статичные поля в AboutPage


# Модель Collection
class Collection(models.Model):
    name = models.CharField(max_length=50, verbose_name='Категория')
    description = models.TextField(default='Описания коллекции', verbose_name='Описания', blank=True, null=True)
    image = models.ImageField(upload_to='photos/collection_avatar/%Y/%m/', verbose_name='photo Коллекции')
    is_published = models.BooleanField(default=True, verbose_name='Публикация')
    slug = models.SlugField(unique=True, null=True, blank=True, verbose_name='Slug', editable=False)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    update_at = models.DateTimeField(auto_now=True, verbose_name='Дата обновления')
    is_new = models.BooleanField(default=False, verbose_name='Новая коллекция')
    
    # SEO поля
    seo_title = models.CharField(
        max_length=70,
        blank=True,
        null=True,
        verbose_name='SEO Title',
        help_text='Заголовок страницы для поисковых систем (рекомендуется до 60 символов)'
    )
    seo_description = models.TextField(
        max_length=160,
        blank=True,
        null=True,
        verbose_name='SEO Description',
        help_text='Описание страницы для поисковых систем (рекомендуется до 160 символов)'
    )

    def save(self, *args, **kwargs):
        # Автогенерация slug из name_uz (основной язык) или name, если name_uz не заполнен
        source_name = getattr(self, 'name_uz', None) or self.name
        
        if source_name:
            need_update_slug = False
            
            if not self.slug:
                need_update_slug = True
            elif self.pk:
                try:
                    old_obj = Collection.objects.get(pk=self.pk)
                    old_name = getattr(old_obj, 'name_uz', None) or old_obj.name
                    if old_name != source_name:
                        need_update_slug = True
                except Collection.DoesNotExist:
                    need_update_slug = True
            
            if need_update_slug:
                self.slug = generate_unique_slug(Collection, source_name, self.pk)
        
        super().save(*args, **kwargs)

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


# Функция для определения пути загрузки изображений галереи ковра
def carpet_gallery_upload_to(instance, filename):
    # Получаем имя коллекции и код ковра
    collection_name = instance.carpet.collection.name
    carpet_code = instance.carpet.code or f'carpet_{instance.carpet.id}'
    # Формируем путь к файлу
    return os.path.join('photos/collections', collection_name, 'gallery', carpet_code, filename)


# Модель для стилей ковров
class Style(models.Model):
    name = models.CharField(max_length=50, verbose_name='Название стиля')
    slug = models.SlugField(unique=True, null=True, blank=True, verbose_name='Slug', editable=False)

    def save(self, *args, **kwargs):
        # Автогенерация slug из name_uz (основной язык) или name, если name_uz не заполнен
        source_name = getattr(self, 'name_uz', None) or self.name
        
        if source_name:
            need_update_slug = False
            
            if not self.slug:
                need_update_slug = True
            elif self.pk:
                try:
                    old_obj = Style.objects.get(pk=self.pk)
                    old_name = getattr(old_obj, 'name_uz', None) or old_obj.name
                    if old_name != source_name:
                        need_update_slug = True
                except Style.DoesNotExist:
                    need_update_slug = True
            
            if need_update_slug:
                self.slug = generate_unique_slug(Style, source_name, self.pk)
        
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Стиль'
        verbose_name_plural = 'Стили'


# Модель для комнат
class Room(models.Model):
    name = models.CharField(max_length=50, verbose_name='Название комнаты')
    slug = models.SlugField(unique=True, null=True, blank=True, verbose_name='Slug', editable=False)

    def save(self, *args, **kwargs):
        # Автогенерация slug из name_uz (основной язык) или name, если name_uz не заполнен
        source_name = getattr(self, 'name_uz', None) or self.name
        
        if source_name:
            need_update_slug = False
            
            if not self.slug:
                need_update_slug = True
            elif self.pk:
                try:
                    old_obj = Room.objects.get(pk=self.pk)
                    old_name = getattr(old_obj, 'name_uz', None) or old_obj.name
                    if old_name != source_name:
                        need_update_slug = True
                except Room.DoesNotExist:
                    need_update_slug = True
            
            if need_update_slug:
                self.slug = generate_unique_slug(Room, source_name, self.pk)
        
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Комната'
        verbose_name_plural = 'Комнаты'


# Модель для цветов
class Color(models.Model):
    name = models.CharField(max_length=50, verbose_name='Название цвета')
    slug = models.SlugField(unique=True, null=True, blank=True, verbose_name='Slug', editable=False)
    hex_code = models.CharField(max_length=7, blank=True, null=True, verbose_name='HEX код цвета',
                                help_text='Например: #FF5733')

    def save(self, *args, **kwargs):
        # Автогенерация slug из name_uz (основной язык) или name, если name_uz не заполнен
        source_name = getattr(self, 'name_uz', None) or self.name
        
        if source_name:
            need_update_slug = False
            
            if not self.slug:
                need_update_slug = True
            elif self.pk:
                try:
                    old_obj = Color.objects.get(pk=self.pk)
                    old_name = getattr(old_obj, 'name_uz', None) or old_obj.name
                    if old_name != source_name:
                        need_update_slug = True
                except Color.DoesNotExist:
                    need_update_slug = True
            
            if need_update_slug:
                self.slug = generate_unique_slug(Color, source_name, self.pk)
        
        super().save(*args, **kwargs)

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
        # Если код не задан, берем его из имени файла изображения
        # Устанавливаем для основного языка (uz) или базового поля code
        if not self.code and not getattr(self, 'code_uz', None) and self.photo:
            # Извлекаем имя файла без расширения
            code_value = self.photo.name.split('/')[-1].split('.')[0]
            # Устанавливаем для основного языка и базового поля
            self.code = code_value
            if hasattr(self, 'code_uz'):
                self.code_uz = code_value
        super(Carpet, self).save(*args, **kwargs)

    def __str__(self):
        return self.code or f'Ковер #{self.id}'

    class Meta:
        verbose_name = 'Ковер'
        verbose_name_plural = 'Ковры'
        ordering = ['-created_at']


# Модель для изображений галереи ковра
class CarpetImage(models.Model):
    """Изображение для галереи ковра"""
    carpet = models.ForeignKey(
        Carpet,
        on_delete=models.CASCADE,
        related_name='gallery_images',
        verbose_name='Ковер'
    )
    image = models.ImageField(
        upload_to=carpet_gallery_upload_to,
        verbose_name='Изображение'
    )
    order = models.PositiveIntegerField(default=0, verbose_name='Порядок сортировки')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    
    def __str__(self):
        return f"Изображение {self.order} - {self.carpet.code or f'Ковер #{self.carpet.id}'}"
    
    class Meta:
        verbose_name = 'Изображение ковра'
        verbose_name_plural = 'Изображения ковра'
        ordering = ['order', 'created_at']


# Модель для изображений новости
def news_image_upload_to(instance, filename):
    """Путь для загрузки изображений новости"""
    return os.path.join('photos/news', f'news_{instance.news.id}', filename)


class NewsImage(models.Model):
    """Изображение для новости"""
    news = models.ForeignKey(
        'News',
        on_delete=models.CASCADE,
        related_name='images',
        verbose_name='Новость'
    )
    image = models.ImageField(
        upload_to=news_image_upload_to,
        verbose_name='Изображение'
    )
    order = models.PositiveIntegerField(default=0, verbose_name='Порядок сортировки')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    
    def __str__(self):
        return f"Изображение {self.order} - {self.news.title or f'Новость #{self.news.id}'}"
    
    class Meta:
        verbose_name = 'Изображение новости'
        verbose_name_plural = 'Изображения новости'
        ordering = ['order', 'created_at']


# Модель для новостей
class News(models.Model):
    title = models.CharField(max_length=200, verbose_name='Заголовок')
    slug = models.SlugField(unique=True, null=True, blank=True, verbose_name='Slug', editable=False)
    
    # Обложка
    cover_image = models.ImageField(
        upload_to='photos/news/%Y/%m/', 
        verbose_name='Обложка', 
        blank=True, 
        null=True,
        help_text='Главное изображение новости'
    )
    
    # Абзацы с форматированием (CKEditor)
    paragraph_1 = models.TextField(
        blank=True,
        null=True,
        verbose_name='Абзац 1',
        help_text='Первый абзац новости. Поддерживает форматирование через CKEditor (жирный, курсив, ссылки, списки и т.д.)'
    )
    paragraph_2 = models.TextField(
        blank=True,
        null=True,
        verbose_name='Абзац 2',
        help_text='Второй абзац новости. Поддерживает форматирование через CKEditor (жирный, курсив, ссылки, списки и т.д.)'
    )
    
    is_published = models.BooleanField(default=True, verbose_name='Публикация')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    update_at = models.DateTimeField(auto_now=True, verbose_name='Дата обновления')
    
    # SEO поля
    seo_title = models.CharField(
        max_length=70,
        blank=True,
        null=True,
        verbose_name='SEO Title',
        help_text='Заголовок страницы для поисковых систем (рекомендуется до 60 символов)'
    )
    seo_description = models.TextField(
        max_length=160,
        blank=True,
        null=True,
        verbose_name='SEO Description',
        help_text='Описание страницы для поисковых систем (рекомендуется до 160 символов)'
    )

    def save(self, *args, **kwargs):
        # Автогенерация slug из title_uz (основной язык) или title, если title_uz не заполнен
        source_title = getattr(self, 'title_uz', None) or getattr(self, 'title', None)
        
        # Преобразуем в строку и проверяем, что не пусто
        if source_title:
            source_title = str(source_title).strip()
            if not source_title:
                source_title = None
        
        if source_title:
            need_update_slug = False
            
            if not self.slug:
                need_update_slug = True
            elif self.pk:
                try:
                    old_obj = News.objects.get(pk=self.pk)
                    old_title = getattr(old_obj, 'title_uz', None) or getattr(old_obj, 'title', None)
                    if old_title:
                        old_title = str(old_title).strip()
                        if not old_title:
                            old_title = None
                    if old_title != source_title:
                        need_update_slug = True
                except News.DoesNotExist:
                    need_update_slug = True
            
            if need_update_slug:
                generated_slug = generate_unique_slug(News, source_title, self.pk)
                # generate_unique_slug всегда возвращает валидный slug или None
                if generated_slug:
                    self.slug = generated_slug
                else:
                    # Если по какой-то причине slug не сгенерирован, создаем fallback
                    self.slug = f"news-{random.randint(10000, 99999)}"
        elif not self.slug:
            # Если title пустой и slug нет, создаем fallback slug
            self.slug = f"news-{random.randint(10000, 99999)}"
        
        # Убеждаемся, что slug всегда валидный перед сохранением
        if not self.slug or not self.slug.strip():
            self.slug = f"news-{random.randint(10000, 99999)}"
        
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Новость'
        verbose_name_plural = 'Новости'
        ordering = ['-created_at']

    def get_absolute_url(self):
        return reverse('catalog:news_detail', kwargs={'news_slug': self.slug})




# Модель для галереи
class Gallery(models.Model):
    title = models.CharField(max_length=200, blank=True, null=True, verbose_name='Название')
    image = models.ImageField(upload_to='photos/gallery/%Y/%m/', verbose_name='Изображение')
    is_published = models.BooleanField(default=True, verbose_name='Публикация')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    order = models.PositiveIntegerField(default=0, verbose_name='Порядок сортировки')
    
    # SEO поля
    seo_title = models.CharField(
        max_length=70,
        blank=True,
        null=True,
        verbose_name='SEO Title',
        help_text='Заголовок страницы для поисковых систем (рекомендуется до 60 символов)'
    )
    seo_description = models.TextField(
        max_length=160,
        blank=True,
        null=True,
        verbose_name='SEO Description',
        help_text='Описание страницы для поисковых систем (рекомендуется до 160 символов)'
    )

    def __str__(self):
        return self.title or f'Изображение #{self.id}'

    class Meta:
        verbose_name = 'Изображение галереи'
        verbose_name_plural = 'Галерея'
        ordering = ['order', '-created_at']


# Нижняя галерея на главной странице (одна запись с 12 фиксированными изображениями)
class MainGallery(models.Model):
    """Нижняя галерея (одна запись)"""

    title = models.CharField(max_length=200, verbose_name="Заголовок")

    image_1 = models.ImageField(
        upload_to="photos/main_gallery/%Y/%m/",
        blank=True,
        null=True,
        verbose_name="Изображение 1",
    )
    image_2 = models.ImageField(
        upload_to="photos/main_gallery/%Y/%m/",
        blank=True,
        null=True,
        verbose_name="Изображение 2",
    )
    image_3 = models.ImageField(
        upload_to="photos/main_gallery/%Y/%m/",
        blank=True,
        null=True,
        verbose_name="Изображение 3",
    )
    image_4 = models.ImageField(
        upload_to="photos/main_gallery/%Y/%m/",
        blank=True,
        null=True,
        verbose_name="Изображение 4",
    )
    image_5 = models.ImageField(
        upload_to="photos/main_gallery/%Y/%m/",
        blank=True,
        null=True,
        verbose_name="Изображение 5",
    )
    image_6 = models.ImageField(
        upload_to="photos/main_gallery/%Y/%m/",
        blank=True,
        null=True,
        verbose_name="Изображение 6",
    )
    image_7 = models.ImageField(
        upload_to="photos/main_gallery/%Y/%m/",
        blank=True,
        null=True,
        verbose_name="Изображение 7",
    )
    image_8 = models.ImageField(
        upload_to="photos/main_gallery/%Y/%m/",
        blank=True,
        null=True,
        verbose_name="Изображение 8",
    )
    image_9 = models.ImageField(
        upload_to="photos/main_gallery/%Y/%m/",
        blank=True,
        null=True,
        verbose_name="Изображение 9",
    )
    image_10 = models.ImageField(
        upload_to="photos/main_gallery/%Y/%m/",
        blank=True,
        null=True,
        verbose_name="Изображение 10",
    )
    image_11 = models.ImageField(
        upload_to="photos/main_gallery/%Y/%m/",
        blank=True,
        null=True,
        verbose_name="Изображение 11",
    )
    image_12 = models.ImageField(
        upload_to="photos/main_gallery/%Y/%m/",
        blank=True,
        null=True,
        verbose_name="Изображение 12",
    )

    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    update_at = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Нижняя галерея"
        verbose_name_plural = "Нижняя галерея"


# Модель для изображений секции "О нас" главной страницы
class AboutImage(models.Model):
    """Изображения для секции 'О нас' на главной странице"""
    homepage = models.ForeignKey(
        'HomePage',
        on_delete=models.CASCADE,
        related_name='about_images',
        verbose_name='Главная страница'
    )
    image = models.ImageField(
        upload_to='photos/homepage/about/%Y/%m/',
        verbose_name='Изображение'
    )
    order = models.PositiveIntegerField(default=0, verbose_name='Порядок сортировки')
    
    def __str__(self):
        return f"Изображение {self.order} для секции 'О нас'"
    
    class Meta:
        verbose_name = 'Изображение секции "О нас"'
        verbose_name_plural = 'Изображения секции "О нас"'
        ordering = ['order']


# Модель для главной страницы
class HomePage(models.Model):
    """Модель главной страницы с мультиязычными полями"""
    
    # ========== СЕКЦИЯ 1: БАННЕР ==========
    # Баннер - переводимые поля
    banner_title = models.CharField(max_length=200, verbose_name='Заголовок баннера')
    banner_description = models.TextField(verbose_name='Описание баннера')
    banner_link = models.CharField(max_length=500, blank=True, verbose_name='Ссылка баннера')
    
    # Баннер - без перевода
    banner_image = models.ImageField(
        upload_to='photos/homepage/banner/%Y/%m/', 
        blank=True, 
        null=True,
        verbose_name='Изображение баннера'
    )
    banner_video = models.FileField(
        upload_to='files/homepage/banner/%Y/%m/', 
        blank=True, 
        null=True,
        verbose_name='Видео баннера'
    )
    
    # Шоурум в баннере - переводимые поля
    banner_showroom_title = models.CharField(max_length=200, verbose_name='Заголовок шоурума')
    
    # Шоурум в баннере - без перевода
    banner_showroom_image = models.ImageField(
        upload_to='photos/homepage/showroom/%Y/%m/', 
        blank=True, 
        null=True,
        verbose_name='Изображение шоурума'
    )
    
    # ========== СЕКЦИЯ 2: О НАС ==========
    # Переводимые поля
    about_section_title = models.CharField(max_length=200, blank=True, null=True, verbose_name='Название секции "О нас"')
    about_title = models.CharField(max_length=200, verbose_name='Заголовок секции "О нас"')
    about_link = models.CharField(max_length=500, blank=True, verbose_name='Ссылка секции "О нас"')
    about_youtube_link = models.CharField(max_length=500, blank=True, verbose_name='Ссылка на YouTube')
    about_bottom_description = models.TextField(verbose_name='Нижнее описание секции "О нас"')
    
    # ========== СЕКЦИЯ 3: ШОУРУМ ==========
    # Без перевода
    showroom_image = models.ImageField(
        upload_to='photos/homepage/showroom_section/%Y/%m/', 
        blank=True, 
        null=True,
        verbose_name='Изображение секции шоурума'
    )
    
    # Переводимые поля
    showroom_title = models.CharField(max_length=200, verbose_name='Заголовок секции шоурума')
    
    # ========== СЕКЦИЯ 4: ПРЕИМУЩЕСТВА (4 карточки) ==========
    # Общие поля секции (переводимые)
    advantage_title = models.CharField(max_length=200, blank=True, null=True, verbose_name='Заголовок секции преимуществ')
    advantage_subtitle = models.CharField(max_length=200, blank=True, null=True, verbose_name='Подзаголовок секции преимуществ')
    
    # Карточка 1
    advantage_1_title = models.CharField(max_length=200, verbose_name='Заголовок карточки 1')
    advantage_1_icon = models.FileField(
        upload_to='icons/homepage/%Y/%m/', 
        blank=True, 
        null=True,
        verbose_name='SVG иконка карточки 1'
    )
    advantage_1_description = models.TextField(verbose_name='Описание карточки 1')
    
    # Карточка 2
    advantage_2_title = models.CharField(max_length=200, verbose_name='Заголовок карточки 2')
    advantage_2_description = models.TextField(verbose_name='Описание карточки 2')
    
    # Карточка 3
    advantage_3_title = models.CharField(max_length=200, verbose_name='Заголовок карточки 3')
    advantage_3_description = models.TextField(verbose_name='Описание карточки 3')
    
    # Карточка 4
    advantage_4_title = models.CharField(max_length=200, verbose_name='Заголовок карточки 4')
    advantage_4_icon = models.FileField(
        upload_to='icons/homepage/%Y/%m/', 
        blank=True, 
        null=True,
        verbose_name='SVG иконка карточки 4'
    )
    advantage_4_description = models.TextField(verbose_name='Описание карточки 4')
    
    # ========== СЕКЦИЯ 5: ПРИЗЫВ К ДЕЙСТВИЮ ==========
    # Переводимые поля
    cta_title = models.CharField(max_length=200, verbose_name='Заголовок призыва к действию')
    cta_description = models.TextField(verbose_name='Описание призыва к действию')
    
    # Изображение (без перевода)
    cta_image = models.ImageField(
        upload_to='photos/homepage/cta/%Y/%m/',
        blank=True,
        null=True,
        verbose_name='Изображение призыва к действию'
    )
    
    # ========== SEO ПОЛЯ ==========
    # Meta теги (переводимые)
    meta_title = models.CharField(
        max_length=70,
        blank=True,
        null=True,
        verbose_name='Meta Title',
        help_text='Заголовок страницы для поисковых систем (рекомендуется до 60 символов)'
    )
    meta_description = models.TextField(
        max_length=160,
        blank=True,
        null=True,
        verbose_name='Meta Description',
        help_text='Описание страницы для поисковых систем (рекомендуется до 160 символов)'
    )
    meta_keywords = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        verbose_name='Meta Keywords',
        help_text='Ключевые слова через запятую'
    )
    
    # Open Graph теги (переводимые)
    og_title = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        verbose_name='OG Title',
        help_text='Заголовок для социальных сетей (Facebook, Twitter и т.д.)'
    )
    og_description = models.TextField(
        max_length=200,
        blank=True,
        null=True,
        verbose_name='OG Description',
        help_text='Описание для социальных сетей'
    )
    
    # Open Graph изображение (без перевода)
    og_image = models.ImageField(
        upload_to='photos/seo/%Y/%m/',
        blank=True,
        null=True,
        verbose_name='OG Image',
        help_text='Изображение для социальных сетей (рекомендуется 1200x630px)'
    )
    
    # Canonical URL (переводимый)
    canonical_url = models.URLField(
        max_length=500,
        blank=True,
        null=True,
        verbose_name='Canonical URL',
        help_text='Канонический URL страницы (опционально)'
    )
    
    # ========== СЛУЖЕБНЫЕ ПОЛЯ ==========
    is_published = models.BooleanField(default=True, verbose_name='Публикация')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    update_at = models.DateTimeField(auto_now=True, verbose_name='Дата обновления')

    def __str__(self):
        return self.banner_title_uz if hasattr(self, 'banner_title_uz') else self.banner_title

    class Meta:
        verbose_name = 'Главная страница'
        verbose_name_plural = 'Главная страница'
        ordering = ['-created_at']


# Модель для страницы "О компании"

class AboutPage(models.Model):
    """Модель страницы о компании - все данные в одной модели"""
    
    # ========== СЕКЦИЯ 1: О КОМПАНИИ ==========
    # Переводимые поля
    about_section_title = models.CharField(max_length=200, blank=True, null=True, verbose_name='Название секции "О компании"')
    about_banner_title = models.CharField(max_length=200, blank=True, null=True, verbose_name='Заголовок баннера')
    about_banner_subtitle = models.CharField(max_length=200, blank=True, null=True, verbose_name='Подзаголовок баннера')
    
    # Изображения (без перевода)
    about_image_1 = models.ImageField(
        upload_to='photos/about/%Y/%m/',
        blank=True,
        null=True,
        verbose_name='Изображение 1'
    )
    about_image_2 = models.ImageField(
        upload_to='photos/about/%Y/%m/',
        blank=True,
        null=True,
        verbose_name='Изображение 2'
    )
    
    # ========== СЕКЦИЯ 2: ПРОЦЕСС ПРОИЗВОДСТВА ==========
    # Переводимые поля
    production_section_title = models.CharField(max_length=200, blank=True, null=True, verbose_name='Название секции "Процесс производства"')
    production_title = models.CharField(max_length=200, blank=True, null=True, verbose_name='Заголовок секции производства')
    
    # ========== СЕКЦИЯ 3: ИСТОРИЯ КОМПАНИИ ==========
    # Переводимые поля
    history_section_title = models.CharField(max_length=200, blank=True, null=True, verbose_name='Название секции "История компании"')
    
    # ========== СЕКЦИЯ 4: ОБЪЕМЫ ПРОИЗВОДСТВА ==========
    # Переводимые поля
    capacity_section_title = models.CharField(max_length=200, blank=True, null=True, verbose_name='Название секции "Объемы производства"')
    capacity_title = models.CharField(max_length=200, blank=True, null=True, verbose_name='Заголовок секции объемов')
    
    # Карточка 1
    capacity_card_1_title = models.CharField(max_length=200, blank=True, null=True, verbose_name='Заголовок карточки 1')
    capacity_card_1_subtitle = models.CharField(max_length=200, blank=True, null=True, verbose_name='Подзаголовок карточки 1')
    capacity_card_1_image = models.ImageField(
        upload_to='photos/production_capacity/%Y/%m/',
        blank=True,
        null=True,
        verbose_name='Изображение карточки 1'
    )
    
    # Карточка 2
    capacity_card_2_title = models.CharField(max_length=200, blank=True, null=True, verbose_name='Заголовок карточки 2')
    capacity_card_2_subtitle = models.CharField(max_length=200, blank=True, null=True, verbose_name='Подзаголовок карточки 2')
    capacity_card_2_image = models.ImageField(
        upload_to='photos/production_capacity/%Y/%m/',
        blank=True,
        null=True,
        verbose_name='Изображение карточки 2'
    )
    
    # Карточка 3
    capacity_card_3_title = models.CharField(max_length=200, blank=True, null=True, verbose_name='Заголовок карточки 3')
    capacity_card_3_subtitle = models.CharField(max_length=200, blank=True, null=True, verbose_name='Подзаголовок карточки 3')
    capacity_card_3_image = models.ImageField(
        upload_to='photos/production_capacity/%Y/%m/',
        blank=True,
        null=True,
        verbose_name='Изображение карточки 3'
    )
    
    # Карточка 4
    capacity_card_4_title = models.CharField(max_length=200, blank=True, null=True, verbose_name='Заголовок карточки 4')
    capacity_card_4_subtitle = models.CharField(max_length=200, blank=True, null=True, verbose_name='Подзаголовок карточки 4')
    capacity_card_4_image = models.ImageField(
        upload_to='photos/production_capacity/%Y/%m/',
        blank=True,
        null=True,
        verbose_name='Изображение карточки 4'
    )
    
    # ========== СЕКЦИЯ 5: ПАРТНЕРСТВО ДЛЯ ДИЛЕРОВ ==========
    # Переводимые поля
    dealer_section_title = models.CharField(max_length=200, blank=True, null=True, verbose_name='Название секции "Партнерство для дилеров"')
    dealer_title = models.CharField(max_length=200, blank=True, null=True, verbose_name='Заголовок секции для дилеров')
    
    # Карточка 1
    dealer_card_1_title = models.CharField(max_length=200, blank=True, null=True, verbose_name='Заголовок карточки 1')
    dealer_card_1_description = models.TextField(blank=True, null=True, verbose_name='Описание карточки 1')
    
    # Карточка 2
    dealer_card_2_title = models.CharField(max_length=200, blank=True, null=True, verbose_name='Заголовок карточки 2')
    dealer_card_2_description = models.TextField(blank=True, null=True, verbose_name='Описание карточки 2')
    
    # Карточка 3
    dealer_card_3_title = models.CharField(max_length=200, blank=True, null=True, verbose_name='Заголовок карточки 3')
    dealer_card_3_description = models.TextField(blank=True, null=True, verbose_name='Описание карточки 3')
    
    # ========== SEO ПОЛЯ ==========
    # Meta теги (переводимые)
    meta_title = models.CharField(
        max_length=70,
        blank=True,
        null=True,
        verbose_name='Meta Title',
        help_text='Заголовок страницы для поисковых систем (рекомендуется до 60 символов)'
    )
    meta_description = models.TextField(
        max_length=160,
        blank=True,
        null=True,
        verbose_name='Meta Description',
        help_text='Описание страницы для поисковых систем (рекомендуется до 160 символов)'
    )
    meta_keywords = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        verbose_name='Meta Keywords',
        help_text='Ключевые слова через запятую'
    )
    
    # Open Graph теги (переводимые)
    og_title = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        verbose_name='OG Title',
        help_text='Заголовок для социальных сетей (Facebook, Twitter и т.д.)'
    )
    og_description = models.TextField(
        max_length=200,
        blank=True,
        null=True,
        verbose_name='OG Description',
        help_text='Описание для социальных сетей'
    )
    
    # Open Graph изображение (без перевода)
    og_image = models.ImageField(
        upload_to='photos/seo/%Y/%m/',
        blank=True,
        null=True,
        verbose_name='OG Image',
        help_text='Изображение для социальных сетей (рекомендуется 1200x630px)'
    )
    
    # Canonical URL (переводимый)
    canonical_url = models.URLField(
        max_length=500,
        blank=True,
        null=True,
        verbose_name='Canonical URL',
        help_text='Канонический URL страницы (опционально)'
    )
    
    # ========== СЛУЖЕБНЫЕ ПОЛЯ ==========
    is_published = models.BooleanField(default=True, verbose_name='Публикация')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    update_at = models.DateTimeField(auto_now=True, verbose_name='Дата обновления')

    def __str__(self):
        return self.about_section_title_uz if hasattr(self, 'about_section_title_uz') else self.about_section_title

    class Meta:
        verbose_name = 'Страница о компании'
        verbose_name_plural = 'Страница о компании'
        ordering = ['-created_at']


# Модель DealerAdvantage удалена - теперь статичные поля в AboutPage


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
        help_text='Например: https://maps.google.com/...',
        max_length=1000,
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
    
    # ========== SEO ПОЛЯ ==========
    # Meta теги (переводимые)
    meta_title = models.CharField(
        max_length=70,
        blank=True,
        null=True,
        verbose_name='Meta Title',
        help_text='Заголовок страницы для поисковых систем (рекомендуется до 60 символов)'
    )
    meta_description = models.TextField(
        max_length=160,
        blank=True,
        null=True,
        verbose_name='Meta Description',
        help_text='Описание страницы для поисковых систем (рекомендуется до 160 символов)'
    )
    meta_keywords = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        verbose_name='Meta Keywords',
        help_text='Ключевые слова через запятую'
    )
    
    # Open Graph теги (переводимые)
    og_title = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        verbose_name='OG Title',
        help_text='Заголовок для социальных сетей (Facebook, Twitter и т.д.)'
    )
    og_description = models.TextField(
        max_length=200,
        blank=True,
        null=True,
        verbose_name='OG Description',
        help_text='Описание для социальных сетей'
    )
    
    # Open Graph изображение (без перевода)
    og_image = models.ImageField(
        upload_to='photos/seo/%Y/%m/',
        blank=True,
        null=True,
        verbose_name='OG Image',
        help_text='Изображение для социальных сетей (рекомендуется 1200x630px)'
    )
    
    # Canonical URL (переводимый)
    canonical_url = models.URLField(
        max_length=500,
        blank=True,
        null=True,
        verbose_name='Canonical URL',
        help_text='Канонический URL страницы (опционально)'
    )
    
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
    slug = models.SlugField(unique=True, null=True, blank=True, verbose_name='Slug', editable=False)
    order = models.PositiveIntegerField(default=0, verbose_name='Порядок сортировки')
    is_published = models.BooleanField(default=True, verbose_name='Публикация')
    
    def save(self, *args, **kwargs):
        # Автогенерация slug из name_uz (основной язык) или name, если name_uz не заполнен
        source_name = getattr(self, 'name_uz', None) or self.name
        
        if source_name:
            need_update_slug = False
            
            if not self.slug:
                need_update_slug = True
            elif self.pk:
                try:
                    old_obj = Region.objects.get(pk=self.pk)
                    old_name = getattr(old_obj, 'name_uz', None) or old_obj.name
                    if old_name != source_name:
                        need_update_slug = True
                except Region.DoesNotExist:
                    need_update_slug = True
            
            if need_update_slug:
                self.slug = generate_unique_slug(Region, source_name, self.pk)
        
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = 'Регион'
        verbose_name_plural = 'Регионы'
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


# Модель для глобальных настроек
class GlobalSettings(models.Model):
    """Модель глобальных настроек сайта (singleton)"""
    
    # Копирайт (мультиязычный)
    copyright = models.CharField(
        max_length=200,
        verbose_name='Копирайт',
        help_text='Текст копирайта в футере сайта'
    )
    
    # Модальное окно формы (мультиязычные поля)
    form_modal_title = models.CharField(
        max_length=200,
        verbose_name='Заголовок модального окна формы',
        help_text='Заголовок модального окна для формы обратной связи'
    )
    form_modal_text = models.TextField(
        verbose_name='Текст модального окна формы',
        help_text='Текст в модальном окне для формы обратной связи'
    )
    
    # Модальное окно успеха (мультиязычные поля)
    success_modal_title = models.CharField(
        max_length=200,
        verbose_name='Заголовок модального окна успеха',
        help_text='Заголовок модального окна после успешной отправки формы'
    )
    success_modal_text = models.TextField(
        verbose_name='Текст модального окна успеха',
        help_text='Текст в модальном окне после успешной отправки формы'
    )
    
    # Контактная информация
    email = models.EmailField(
        verbose_name='Email',
        help_text='Email для связи'
    )
    address = models.TextField(
        verbose_name='Адрес',
        help_text='Адрес компании'
    )
    phone = models.CharField(
        max_length=50,
        verbose_name='Номер телефона',
        help_text='Номер телефона для связи'
    )
    
    # 3D тур
    tour_3d_link = models.URLField(
        max_length=500,
        blank=True,
        null=True,
        verbose_name='Ссылка на 3D тур',
        help_text='Ссылка на 3D тур (опционально)'
    )
    
    # Обложки страниц
    collection_cover_image = models.ImageField(
        upload_to='photos/global_settings/%Y/%m/',
        blank=True,
        null=True,
        verbose_name='Обложка страницы коллекции',
        help_text='Изображение обложки для страницы коллекций'
    )
    product_cover_image = models.ImageField(
        upload_to='photos/global_settings/%Y/%m/',
        blank=True,
        null=True,
        verbose_name='Обложка страницы продуктов',
        help_text='Изображение обложки для страницы продуктов'
    )
    
    # Служебные поля
    is_published = models.BooleanField(default=True, verbose_name='Публикация')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    update_at = models.DateTimeField(auto_now=True, verbose_name='Дата обновления')
    
    def __str__(self):
        return 'Глобальные настройки'
    
    class Meta:
        verbose_name = 'Глобальные настройки'
        verbose_name_plural = 'Глобальные настройки'
        ordering = ['-created_at']
