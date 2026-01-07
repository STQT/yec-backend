from django.db import models
from django.urls import reverse
import os


# Модель для типов ковров
class TypeCarpetCollection(models.Model):
    type = models.CharField(max_length=32, verbose_name='Тип ковра')
    slug = models.SlugField(unique=True, null=True, verbose_name='Slug')
    description = models.TextField(default='Описания ковра', verbose_name='Описания', blank=True, null=True)
    image = models.ImageField(upload_to='photos/typecarpet_avatar/%Y/%m/', verbose_name='photo тип ковров', blank=True)

    def __str__(self):
        return self.type

    class Meta:
        verbose_name = 'Тип ковра'
        verbose_name_plural = 'Типы ковров'

    def get_absolute_url(self):
        return reverse('catalog:typecarpet', kwargs={'typecarpet_slug': self.slug})


# Модель Collection
class Collection(models.Model):
    name = models.CharField(max_length=50, verbose_name='Категория')
    description = models.TextField(default='Описания коллекции', verbose_name='Описания', blank=True, null=True)
    image = models.ImageField(upload_to='photos/collection_avatar/%Y/%m/', verbose_name='photo Коллекции')
    type = models.ForeignKey(TypeCarpetCollection, on_delete=models.CASCADE, verbose_name='Тип ковра')
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
    content = models.TextField(blank=True, null=True, verbose_name='Содержание')
    image = models.ImageField(upload_to='photos/news/%Y/%m/', verbose_name='Изображение', blank=True, null=True)
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


# Модель для галереи
class Gallery(models.Model):
    title = models.CharField(max_length=200, blank=True, null=True, verbose_name='Название')
    image = models.ImageField(upload_to='photos/gallery/%Y/%m/', verbose_name='Изображение')
    description = models.TextField(blank=True, null=True, verbose_name='Описание')
    is_published = models.BooleanField(default=True, verbose_name='Публикация')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    order = models.PositiveIntegerField(default=0, verbose_name='Порядок сортировки')

    def __str__(self):
        return self.title or f'Изображение #{self.id}'

    class Meta:
        verbose_name = 'Изображение галереи'
        verbose_name_plural = 'Галерея'
        ordering = ['order', '-created_at']
