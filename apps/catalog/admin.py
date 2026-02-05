from django.contrib import admin
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.utils.html import format_html
from django.utils.safestring import mark_safe

from apps.catalog.models import (
    AboutImage,
    AboutPage,
    AdvantageCard,
    Carpet,
    CarpetImage,
    Collection,
    Color,
    CompanyHistory,
    ContactFormSubmission,
    ContactPage,
    FAQ,
    Gallery,
    GlobalSettings,
    HomePage,
    InstagramPost,
    MainGallery,
    News,
    NewsImage,
    ProductionStep,
    Region,
    Room,
    SalesPoint,
    Style,
)


@admin.register(Collection)
class CollectionAdmin(admin.ModelAdmin):
    """Админка для коллекций"""
    list_display = ["image_preview", "name", "slug", "is_published", "is_new", "carpets_count", "created_at"]
    list_display_links = ["image_preview", "name"]
    list_filter = ["is_published", "is_new", "created_at"]
    search_fields = ["name", "description"]
    readonly_fields = ["image_preview", "slug", "created_at", "update_at", "carpets_count"]
    date_hierarchy = "created_at"
    fieldsets = (
        ("Основная информация", {
            "fields": (
                "name_uz",
                "name_ru",
                "name_en",
                "slug",
                "description_uz",
                "description_ru",
                "description_en"
            )
        }),
        ("Изображение", {
            "fields": ("image", "image_preview")
        }),
        ("SEO", {
            "fields": (
                "seo_title_uz",
                "seo_title_ru",
                "seo_title_en",
                "seo_description_uz",
                "seo_description_ru",
                "seo_description_en",
            )
        }),
        ("Настройки", {
            "fields": ("is_published", "is_new")
        }),
        ("Даты", {
            "fields": ("created_at", "update_at")
        }),
    )

    def image_preview(self, obj):
        """Превью изображения"""
        if obj.image:
            return format_html(
                '<img src="{}" style="max-width: 100px; max-height: 100px; object-fit: cover; border-radius: 4px;"/>',
                obj.image.url
            )
        return "-"
    image_preview.short_description = "Превью"

    def carpets_count(self, obj):
        """Количество ковров в коллекции"""
        return obj.carpets.count()
    carpets_count.short_description = "Количество ковров"


@admin.register(Style)
class StyleAdmin(admin.ModelAdmin):
    """Админка для стилей"""
    list_display = ["name", "slug", "carpets_count"]
    list_display_links = ["name"]
    search_fields = ["name"]
    readonly_fields = ["carpets_count"]
    
    fieldsets = (
        ("Название стиля", {
            "fields": (
                "name_uz",
                "name_ru",
                "name_en",
            )
        }),
    )
    
    def get_readonly_fields(self, request, obj=None):
        """Slug показывается только при редактировании существующего объекта"""
        readonly = list(self.readonly_fields)
        if obj:  # Если объект существует, показываем slug
            readonly.append("slug")
        return readonly

    def carpets_count(self, obj):
        """Количество ковров со стилем"""
        return obj.carpets.count()
    carpets_count.short_description = "Количество ковров"


@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    """Админка для комнат"""
    list_display = ["name", "slug", "carpets_count"]
    list_display_links = ["name"]
    search_fields = ["name"]
    readonly_fields = ["carpets_count"]
    
    fieldsets = (
        ("Название комнаты", {
            "fields": (
                "name_uz",
                "name_ru",
                "name_en",
            )
        }),
    )
    
    def get_readonly_fields(self, request, obj=None):
        """Slug показывается только при редактировании существующего объекта"""
        readonly = list(self.readonly_fields)
        if obj:  # Если объект существует, показываем slug
            readonly.append("slug")
        return readonly

    def carpets_count(self, obj):
        """Количество ковров для комнаты"""
        return obj.carpets.count()
    carpets_count.short_description = "Количество ковров"


@admin.register(Color)
class ColorAdmin(admin.ModelAdmin):
    """Админка для цветов"""
    list_display = ["color_preview", "name", "slug", "hex_code", "carpets_count"]
    list_display_links = ["name"]
    search_fields = ["name"]
    readonly_fields = ["color_preview", "carpets_count"]
    
    fieldsets = (
        ("Название цвета", {
            "fields": (
                "name_uz",
                "name_ru",
                "name_en",
            )
        }),
        ("Цвет", {
            "fields": ("hex_code", "color_preview")
        }),
    )
    
    def get_readonly_fields(self, request, obj=None):
        """Slug показывается только при редактировании существующего объекта"""
        readonly = list(self.readonly_fields)
        if obj:  # Если объект существует, показываем slug
            readonly.append("slug")
        return readonly

    def color_preview(self, obj):
        """Превью цвета"""
        if obj and obj.hex_code:
            return format_html(
                '<div style="width: 30px; height: 30px; background-color: {}; border-radius: 4px; border: 1px solid #ddd;"></div>',
                obj.hex_code
            )
        return "-"
    color_preview.short_description = "Цвет"

    def carpets_count(self, obj):
        """Количество ковров с цветом"""
        return obj.carpets.count()
    carpets_count.short_description = "Количество ковров"


class CarpetImageInline(admin.StackedInline):
    """Inline для изображений галереи ковра"""
    model = CarpetImage
    extra = 1
    fields = ["image", "order", "image_preview"]
    readonly_fields = ["image_preview"]
    ordering = ["order"]
    
    def image_preview(self, obj):
        """Превью изображения"""
        if obj and obj.image:
            return format_html(
                '<img src="{}" style="max-width: 150px; max-height: 150px; object-fit: cover; border-radius: 4px;"/>',
                obj.image.url
            )
        return "-"
    image_preview.short_description = "Превью"


@admin.register(Carpet)
class CarpetAdmin(admin.ModelAdmin):
    """Админка для ковров"""
    inlines = [CarpetImageInline]
    list_display = [
        "photo_preview",
        "code",
        "collection",
        "material",
        "is_new",
        "is_popular",
        "is_published",
        "watched",
        "created_at"
    ]
    list_display_links = ["photo_preview", "code"]
    list_filter = [
        "is_published",
        "is_new",
        "is_popular",
        "collection",
        "styles",
        "rooms",
        "colors",
        "roll",
        "created_at"
    ]
    search_fields = ["code", "material", "collection__name"]
    readonly_fields = [
        "photo_preview",
        "watched",
        "created_at",
        "update_at"
    ]
    filter_horizontal = ["styles", "rooms", "colors"]
    date_hierarchy = "created_at"
    fieldsets = (
        ("Основная информация", {
            "fields": (
                "code_uz",
                "code_ru",
                "code_en",
                "collection",
                "roll"
            )
        }),
        ("Изображение", {
            "fields": ("photo", "photo_preview")
        }),
        ("Характеристики", {
            "fields": (
                "material_uz",
                "material_ru",
                "material_en",
                "density_uz",
                "density_ru",
                "density_en",
                "base_uz",
                "base_ru",
                "base_en",
                "pile_height_uz",
                "pile_height_ru",
                "pile_height_en",
                "yarn_composition_uz",
                "yarn_composition_ru",
                "yarn_composition_en",
                "weight_uz",
                "weight_ru",
                "weight_en"
            )
        }),
        ("Фильтры", {
            "fields": ("styles", "rooms", "colors", "is_new", "is_popular")
        }),
        ("Статистика", {
            "fields": ("watched",)
        }),
        ("Настройки", {
            "fields": ("is_published",)
        }),
        ("Даты", {
            "fields": ("created_at", "update_at")
        }),
    )

    def photo_preview(self, obj):
        """Превью изображения ковра"""
        if obj.photo:
            return format_html(
                '<img src="{}" style="max-width: 150px; max-height: 150px; object-fit: cover; border-radius: 4px;"/>',
                obj.photo.url
            )
        return "-"
    photo_preview.short_description = "Превью"


class NewsImageInline(admin.StackedInline):
    """Inline для изображений новости"""
    model = NewsImage
    extra = 1
    fields = ["image", "order", "image_preview"]
    readonly_fields = ["image_preview"]
    ordering = ["order"]
    
    def image_preview(self, obj):
        """Превью изображения"""
        if obj and obj.image:
            return format_html(
                '<img src="{}" style="max-width: 150px; max-height: 150px; object-fit: cover; border-radius: 4px;"/>',
                obj.image.url
            )
        return "-"
    image_preview.short_description = "Превью"


@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    """Админка для новостей с CKEditor"""
    inlines = [NewsImageInline]
    list_display = ["cover_image_preview", "title", "slug", "is_published", "created_at"]
    list_display_links = ["title"]
    list_filter = ["is_published", "created_at"]
    search_fields = ["title_uz", "title_ru", "title_en"]
    readonly_fields = ["cover_image_preview", "created_at", "update_at"]
    date_hierarchy = "created_at"
    
    fieldsets = (
        ("Основная информация", {
            "fields": ("title_uz", "title_ru", "title_en")
        }),
        ("Обложка", {
            "fields": ("cover_image", "cover_image_preview"),
            "description": "Главное изображение новости"
        }),
        ("Абзац 1", {
            "fields": ("paragraph_1_uz", "paragraph_1_ru", "paragraph_1_en"),
            "description": "Первый абзац новости. Поддерживает форматирование через CKEditor (жирный, курсив, ссылки, списки и т.д.)"
        }),
        ("Абзац 2", {
            "fields": ("paragraph_2_uz", "paragraph_2_ru", "paragraph_2_en"),
            "description": "Второй абзац новости. Поддерживает форматирование через CKEditor (жирный, курсив, ссылки, списки и т.д.)"
        }),
        ("SEO", {
            "fields": (
                "seo_title_uz",
                "seo_title_ru",
                "seo_title_en",
                "seo_description_uz",
                "seo_description_ru",
                "seo_description_en",
            )
        }),
        ("Настройки", {
            "fields": ("is_published",)
        }),
        ("Даты", {
            "fields": ("created_at", "update_at")
        }),
    )
    
    class Media:
        js = (
            'https://cdnjs.cloudflare.com/ajax/libs/tinymce/6.8.3/tinymce.min.js',
            'js/ckeditor_init.js',
        )
    
    def get_readonly_fields(self, request, obj=None):
        """Slug показывается только при редактировании существующего объекта"""
        readonly = list(self.readonly_fields)
        if obj:  # Если объект существует, показываем slug
            readonly.append("slug")
        return readonly
    
    def save_model(self, request, obj, form, change):
        """Переопределяем сохранение для обработки ошибок"""
        # Убеждаемся, что slug всегда валидный перед сохранением
        if not obj.slug or not obj.slug.strip():
            from apps.catalog.models import generate_unique_slug
            import random
            source_title = getattr(obj, 'title_uz', None) or getattr(obj, 'title', None)
            if source_title:
                obj.slug = generate_unique_slug(type(obj), str(source_title).strip(), obj.pk)
            if not obj.slug or not obj.slug.strip():
                obj.slug = f"news-{random.randint(10000, 99999)}"
        
        try:
            super().save_model(request, obj, form, change)
        except Exception as e:
            # Если произошла ошибка при сохранении, логируем и показываем пользователю
            import logging
            logger = logging.getLogger(__name__)
            logger.error(f"Ошибка при сохранении новости: {str(e)}", exc_info=True)
            # Если slug пустой или None, генерируем его заново
            if not obj.slug or not obj.slug.strip():
                from apps.catalog.models import generate_unique_slug
                import random
                source_title = getattr(obj, 'title_uz', None) or getattr(obj, 'title', None)
                if source_title:
                    obj.slug = generate_unique_slug(type(obj), str(source_title).strip(), obj.pk)
                if not obj.slug or not obj.slug.strip():
                    obj.slug = f"news-{random.randint(10000, 99999)}"
            # Пытаемся сохранить снова
            try:
                super().save_model(request, obj, form, change)
            except Exception as e2:
                # Если все еще ошибка, пробрасываем её дальше
                logger.error(f"Критическая ошибка при сохранении новости: {str(e2)}", exc_info=True)
                raise

    def cover_image_preview(self, obj):
        """Превью обложки"""
        if obj and obj.cover_image:
            return format_html(
                '<img src="{}" style="max-width: 150px; max-height: 150px; object-fit: cover; border-radius: 4px;"/>',
                obj.cover_image.url
            )
        return "-"
    cover_image_preview.short_description = "Превью обложки"


@admin.register(Gallery)
class GalleryAdmin(admin.ModelAdmin):
    """Админка для галереи"""
    list_display = ["image_preview", "title", "order", "is_published", "created_at"]
    list_display_links = ["title", "image_preview"]
    list_filter = ["is_published", "created_at"]
    search_fields = ["title_uz", "title_ru", "title_en"]
    readonly_fields = ["image_preview", "created_at"]
    list_editable = ["order", "is_published"]
    fieldsets = (
        ("Основная информация", {
            "fields": (
                "title_uz",
                "title_ru",
                "title_en",
                "order"
            )
        }),
        ("Изображение", {
            "fields": ("image", "image_preview")
        }),
        ("Настройки", {
            "fields": ("is_published",)
        }),
        ("Даты", {
            "fields": ("created_at",)
        }),
    )

    def image_preview(self, obj):
        """Превью изображения"""
        if obj.image:
            return format_html(
                '<img src="{}" style="max-width: 200px; max-height: 200px; object-fit: cover; border-radius: 4px;"/>',
                obj.image.url
            )
        return "-"
    image_preview.short_description = "Превью"

    class Meta:
        ordering = ["order", "-created_at"]


@admin.register(MainGallery)
class MainGalleryAdmin(admin.ModelAdmin):
    """Админка для нижней галереи (одна запись)"""
    list_display = ["title", "created_at"]
    list_display_links = ["title"]
    readonly_fields = [
        "image_1_preview",
        "image_2_preview",
        "image_3_preview",
        "image_4_preview",
        "image_5_preview",
        "image_6_preview",
        "image_7_preview",
        "image_8_preview",
        "image_9_preview",
        "image_10_preview",
        "image_11_preview",
        "image_12_preview",
        "created_at",
        "update_at"
    ]
    fieldsets = (
        ("Заголовок", {"fields": ("title_uz", "title_ru", "title_en")}),
        (
            "Изображения",
            {
                "fields": (
                    "image_1",
                    "image_1_preview",
                    "image_2",
                    "image_2_preview",
                    "image_3",
                    "image_3_preview",
                    "image_4",
                    "image_4_preview",
                    "image_5",
                    "image_5_preview",
                    "image_6",
                    "image_6_preview",
                    "image_7",
                    "image_7_preview",
                    "image_8",
                    "image_8_preview",
                    "image_9",
                    "image_9_preview",
                    "image_10",
                    "image_10_preview",
                    "image_11",
                    "image_11_preview",
                    "image_12",
                    "image_12_preview",
                )
            },
        ),
        ("Служебное", {"fields": ("created_at", "update_at"), "classes": ("collapse",)}),
    )
    
    def has_add_permission(self, request):
        """Разрешаем добавление только если нет записей"""
        return MainGallery.objects.count() == 0

    def has_delete_permission(self, request, obj=None):
        """Запрещаем удаление, так как должна быть только одна запись"""
        return False

    def changelist_view(self, request, extra_context=None):
        """Открывать сразу форму редактирования (или создание, если записи нет)"""
        obj = MainGallery.objects.first()
        if obj:
            return HttpResponseRedirect(reverse("admin:catalog_maingallery_change", args=[obj.pk]))
        return HttpResponseRedirect(reverse("admin:catalog_maingallery_add"))
    
    def image_1_preview(self, obj):
        """Превью первого изображения"""
        if obj and obj.image_1:
            return format_html(
                '<img src="{}" style="max-width: 300px; max-height: 200px; object-fit: cover; border-radius: 4px;"/>',
                obj.image_1.url
            )
        return "-"
    image_1_preview.short_description = "Превью изображения 1"
    
    def image_2_preview(self, obj):
        """Превью второго изображения"""
        if obj and obj.image_2:
            return format_html(
                '<img src="{}" style="max-width: 300px; max-height: 200px; object-fit: cover; border-radius: 4px;"/>',
                obj.image_2.url
            )
        return "-"
    image_2_preview.short_description = "Превью изображения 2"
    
    def image_3_preview(self, obj):
        """Превью третьего изображения"""
        if obj and obj.image_3:
            return format_html(
                '<img src="{}" style="max-width: 300px; max-height: 200px; object-fit: cover; border-radius: 4px;"/>',
                obj.image_3.url
            )
        return "-"
    image_3_preview.short_description = "Превью изображения 3"
    
    def image_4_preview(self, obj):
        """Превью четвертого изображения"""
        if obj and obj.image_4:
            return format_html(
                '<img src="{}" style="max-width: 300px; max-height: 200px; object-fit: cover; border-radius: 4px;"/>',
                obj.image_4.url
            )
        return "-"
    image_4_preview.short_description = "Превью изображения 4"
    
    def image_5_preview(self, obj):
        """Превью пятого изображения"""
        if obj and obj.image_5:
            return format_html(
                '<img src="{}" style="max-width: 300px; max-height: 200px; object-fit: cover; border-radius: 4px;"/>',
                obj.image_5.url
            )
        return "-"
    image_5_preview.short_description = "Превью изображения 5"
    
    def image_6_preview(self, obj):
        """Превью шестого изображения"""
        if obj and obj.image_6:
            return format_html(
                '<img src="{}" style="max-width: 300px; max-height: 200px; object-fit: cover; border-radius: 4px;"/>',
                obj.image_6.url
            )
        return "-"
    image_6_preview.short_description = "Превью изображения 6"
    
    def image_7_preview(self, obj):
        """Превью седьмого изображения"""
        if obj and obj.image_7:
            return format_html(
                '<img src="{}" style="max-width: 300px; max-height: 200px; object-fit: cover; border-radius: 4px;"/>',
                obj.image_7.url
            )
        return "-"
    image_7_preview.short_description = "Превью изображения 7"
    
    def image_8_preview(self, obj):
        """Превью восьмого изображения"""
        if obj and obj.image_8:
            return format_html(
                '<img src="{}" style="max-width: 300px; max-height: 200px; object-fit: cover; border-radius: 4px;"/>',
                obj.image_8.url
            )
        return "-"
    image_8_preview.short_description = "Превью изображения 8"
    
    def image_9_preview(self, obj):
        """Превью девятого изображения"""
        if obj and obj.image_9:
            return format_html(
                '<img src="{}" style="max-width: 300px; max-height: 200px; object-fit: cover; border-radius: 4px;"/>',
                obj.image_9.url
            )
        return "-"
    image_9_preview.short_description = "Превью изображения 9"
    
    def image_10_preview(self, obj):
        """Превью десятого изображения"""
        if obj and obj.image_10:
            return format_html(
                '<img src="{}" style="max-width: 300px; max-height: 200px; object-fit: cover; border-radius: 4px;"/>',
                obj.image_10.url
            )
        return "-"
    image_10_preview.short_description = "Превью изображения 10"
    
    def image_11_preview(self, obj):
        """Превью одиннадцатого изображения"""
        if obj and obj.image_11:
            return format_html(
                '<img src="{}" style="max-width: 300px; max-height: 200px; object-fit: cover; border-radius: 4px;"/>',
                obj.image_11.url
            )
        return "-"
    image_11_preview.short_description = "Превью изображения 11"
    
    def image_12_preview(self, obj):
        """Превью двенадцатого изображения"""
        if obj and obj.image_12:
            return format_html(
                '<img src="{}" style="max-width: 300px; max-height: 200px; object-fit: cover; border-radius: 4px;"/>',
                obj.image_12.url
            )
        return "-"
    image_12_preview.short_description = "Превью изображения 12"


class AboutImageInline(admin.StackedInline):
    """Inline для изображений секции 'О нас'"""
    model = AboutImage
    extra = 1
    fields = ["image", "order", "image_preview"]
    readonly_fields = ["image_preview"]
    ordering = ["order"]
    
    def image_preview(self, obj):
        """Превью изображения"""
        if obj and obj.image:
            return format_html(
                '<img src="{}" style="max-width: 150px; max-height: 150px; object-fit: cover; border-radius: 4px;"/>',
                obj.image.url
            )
        return "-"
    image_preview.short_description = "Превью"


@admin.register(HomePage)
class HomePageAdmin(admin.ModelAdmin):
    """Админка для главной страницы с табами"""
    inlines = [AboutImageInline]
    list_display = ["banner_title_preview", "is_published", "created_at"]
    list_display_links = ["banner_title_preview"]
    list_filter = ["is_published", "created_at"]
    search_fields = ["banner_title_uz", "banner_title_ru", "banner_title_en"]
    readonly_fields = [
        "banner_image_preview",
        "banner_showroom_image_preview",
        "showroom_image_preview",
        "cta_image_preview",
        "og_image_preview",
        "created_at",
        "update_at"
    ]
    date_hierarchy = "created_at"
    
    fieldsets = (
        # ========== ТАБ 1: БАННЕР ==========
        ("Баннер", {
            "fields": (
                "banner_title_uz",
                "banner_title_ru",
                "banner_title_en",
                "banner_description_uz",
                "banner_description_ru",
                "banner_description_en",
                "banner_link_uz",
                "banner_link_ru",
                "banner_link_en",
                "banner_image",
                "banner_image_preview",
                "banner_video",
                "banner_showroom_title_uz",
                "banner_showroom_title_ru",
                "banner_showroom_title_en",
                "banner_showroom_image",
                "banner_showroom_image_preview",
            )
        }),
        # ========== ТАБ 2: О НАС ==========
        ("О нас", {
            "fields": (
                "about_section_title_uz",
                "about_section_title_ru",
                "about_section_title_en",
                "about_title_uz",
                "about_title_ru",
                "about_title_en",
                "about_link_uz",
                "about_link_ru",
                "about_link_en",
                "about_youtube_link_uz",
                "about_youtube_link_ru",
                "about_youtube_link_en",
                "about_bottom_description_uz",
                "about_bottom_description_ru",
                "about_bottom_description_en",
            )
        }),
        # ========== ТАБ 3: ШОУРУМ ==========
        ("Шоурум", {
            "fields": (
                "showroom_image",
                "showroom_image_preview",
                "showroom_title_uz",
                "showroom_title_ru",
                "showroom_title_en",
            )
        }),
        # ========== ТАБ 4: ПРЕИМУЩЕСТВА ==========
        ("Преимущества", {
            "fields": (
                # Общие поля секции
                "advantage_title_uz",
                "advantage_title_ru",
                "advantage_title_en",
                "advantage_subtitle_uz",
                "advantage_subtitle_ru",
                "advantage_subtitle_en",
                # Карточка 1
                "advantage_1_title_uz",
                "advantage_1_title_ru",
                "advantage_1_title_en",
                "advantage_1_icon",
                "advantage_1_description_uz",
                "advantage_1_description_ru",
                "advantage_1_description_en",
                # Карточка 2
                "advantage_2_title_uz",
                "advantage_2_title_ru",
                "advantage_2_title_en",
                "advantage_2_description_uz",
                "advantage_2_description_ru",
                "advantage_2_description_en",
                # Карточка 3
                "advantage_3_title_uz",
                "advantage_3_title_ru",
                "advantage_3_title_en",
                "advantage_3_description_uz",
                "advantage_3_description_ru",
                "advantage_3_description_en",
                # Карточка 4
                "advantage_4_title_uz",
                "advantage_4_title_ru",
                "advantage_4_title_en",
                "advantage_4_icon",
                "advantage_4_description_uz",
                "advantage_4_description_ru",
                "advantage_4_description_en",
            )
        }),
        # ========== ТАБ 5: ПРИЗЫВ К ДЕЙСТВИЮ ==========
        ("Призыв к действию", {
            "fields": (
                "cta_title_uz",
                "cta_title_ru",
                "cta_title_en",
                "cta_description_uz",
                "cta_description_ru",
                "cta_description_en",
                "cta_image",
                "cta_image_preview",
            )
        }),
        # ========== ТАБ 6: SEO ==========
        ("SEO", {
            "fields": (
                "meta_title_uz",
                "meta_title_ru",
                "meta_title_en",
                "meta_description_uz",
                "meta_description_ru",
                "meta_description_en",
                "meta_keywords_uz",
                "meta_keywords_ru",
                "meta_keywords_en",
                "og_title_uz",
                "og_title_ru",
                "og_title_en",
                "og_description_uz",
                "og_description_ru",
                "og_description_en",
                "og_image",
                "og_image_preview",
                "canonical_url_uz",
                "canonical_url_ru",
                "canonical_url_en",
            ),
            "description": "Настройки для поисковых систем и социальных сетей"
        }),
        # ========== НАСТРОЙКИ ==========
        ("Настройки", {
            "fields": ("is_published", "created_at", "update_at"),
            # не делаем collapse, чтобы табы корректно работали
        }),
    )
    
    def changelist_view(self, request, extra_context=None):
        """Перенаправляем на форму редактирования, если есть запись, или на создание"""
        obj = HomePage.objects.first()
        if obj:
            return HttpResponseRedirect(
                reverse('admin:catalog_homepage_change', args=[obj.pk])
            )
        return HttpResponseRedirect(
            reverse('admin:catalog_homepage_add')
        )
    
    def has_add_permission(self, request):
        """Разрешаем добавление только если нет записей"""
        return HomePage.objects.count() == 0
    
    def has_delete_permission(self, request, obj=None):
        """Запрещаем удаление, так как должна быть только одна запись"""
        return False
    
    def banner_title_preview(self, obj):
        """Превью заголовка для списка"""
        if obj:
            return obj.banner_title_uz if hasattr(obj, 'banner_title_uz') else obj.banner_title
        return "-"
    banner_title_preview.short_description = "Заголовок"
    
    def banner_image_preview(self, obj):
        """Превью изображения баннера"""
        if obj and obj.banner_image:
            return format_html(
                '<img src="{}" style="max-width: 300px; max-height: 200px; object-fit: cover; border-radius: 4px;"/>',
                obj.banner_image.url
            )
        return "-"
    banner_image_preview.short_description = "Превью изображения баннера"
    
    def banner_showroom_image_preview(self, obj):
        """Превью изображения шоурума в баннере"""
        if obj and obj.banner_showroom_image:
            return format_html(
                '<img src="{}" style="max-width: 300px; max-height: 200px; object-fit: cover; border-radius: 4px;"/>',
                obj.banner_showroom_image.url
            )
        return "-"
    banner_showroom_image_preview.short_description = "Превью изображения шоурума"
    
    def showroom_image_preview(self, obj):
        """Превью изображения секции шоурума"""
        if obj and obj.showroom_image:
            return format_html(
                '<img src="{}" style="max-width: 300px; max-height: 200px; object-fit: cover; border-radius: 4px;"/>',
                obj.showroom_image.url
            )
        return "-"
    showroom_image_preview.short_description = "Превью изображения шоурума"
    
    def cta_image_preview(self, obj):
        """Превью изображения призыва к действию"""
        if obj and obj.cta_image:
            return format_html(
                '<img src="{}" style="max-width: 300px; max-height: 200px; object-fit: cover; border-radius: 4px;"/>',
                obj.cta_image.url
            )
        return "-"
    cta_image_preview.short_description = "Превью изображения"
    
    def og_image_preview(self, obj):
        """Превью OG изображения"""
        if obj and obj.og_image:
            return format_html(
                '<img src="{}" style="max-width: 300px; max-height: 200px; object-fit: cover; border-radius: 4px;"/>',
                obj.og_image.url
            )
        return "-"
    og_image_preview.short_description = "Превью OG изображения"


class ProductionStepInline(admin.StackedInline):
    """Inline для этапов производства"""
    model = ProductionStep
    extra = 1
    fields = [
        "order",
        "title_uz",
        "title_ru",
        "title_en",
        "description_uz",
        "description_ru",
        "description_en",
        "image"
    ]
    ordering = ["order"]


class CompanyHistoryInline(admin.StackedInline):
    """Inline для истории компании"""
    model = CompanyHistory
    extra = 1
    fields = [
        "year",
        "year_title_uz",
        "year_title_ru",
        "year_title_en",
        "year_description_uz",
        "year_description_ru",
        "year_description_en",
        "image",
        "image_preview",
    ]
    readonly_fields = ["image_preview"]
    ordering = ["year"]
    verbose_name = "Событие истории"
    verbose_name_plural = "События истории"
    
    def image_preview(self, obj):
        """Превью изображения"""
        if obj and obj.image:
            return format_html(
                '<img src="{}" style="max-width: 150px; max-height: 150px; object-fit: cover; border-radius: 4px;"/>',
                obj.image.url
            )
        return "-"
    image_preview.short_description = "Превью"


@admin.register(AboutPage)
class AboutPageAdmin(admin.ModelAdmin):
    """Админка для страницы о компании"""
    list_display = ["about_section_title_preview", "is_published", "created_at"]
    list_display_links = ["about_section_title_preview"]
    list_filter = ["is_published", "created_at"]
    search_fields = ["about_section_title_uz", "about_banner_title_uz"]
    readonly_fields = [
        "about_image_1_preview",
        "about_image_2_preview",
        "capacity_card_1_image_preview",
        "capacity_card_2_image_preview",
        "capacity_card_3_image_preview",
        "capacity_card_4_image_preview",
        "og_image_preview",
        "created_at",
        "update_at"
    ]
    date_hierarchy = "created_at"
    inlines = [ProductionStepInline, CompanyHistoryInline]
    fieldsets = (
        # ========== СЕКЦИЯ 1: О КОМПАНИИ ==========
        ("О компании", {
            "fields": (
                "about_section_title_uz",
                "about_section_title_ru",
                "about_section_title_en",
                "about_banner_title_uz",
                "about_banner_title_ru",
                "about_banner_title_en",
                "about_banner_subtitle_uz",
                "about_banner_subtitle_ru",
                "about_banner_subtitle_en",
                "about_image_1",
                "about_image_1_preview",
                "about_image_2",
                "about_image_2_preview",
            )
        }),
        # ========== СЕКЦИЯ 2: ПРОЦЕСС ПРОИЗВОДСТВА ==========
        ("Процесс производства", {
            "fields": (
                "production_section_title_uz",
                "production_section_title_ru",
                "production_section_title_en",
                "production_title_uz",
                "production_title_ru",
                "production_title_en",
            )
        }),
        # ========== СЕКЦИЯ 3: ИСТОРИЯ КОМПАНИИ ==========
        ("История компании", {
            "fields": (
                "history_section_title_uz",
                "history_section_title_ru",
                "history_section_title_en",
            )
        }),
        # ========== СЕКЦИЯ 4: ОБЪЕМЫ ПРОИЗВОДСТВА ==========
        ("Объемы производства", {
            "fields": (
                "capacity_section_title_uz",
                "capacity_section_title_ru",
                "capacity_section_title_en",
                "capacity_title_uz",
                "capacity_title_ru",
                "capacity_title_en",
                # Карточка 1
                "capacity_card_1_title_uz",
                "capacity_card_1_title_ru",
                "capacity_card_1_title_en",
                "capacity_card_1_subtitle_uz",
                "capacity_card_1_subtitle_ru",
                "capacity_card_1_subtitle_en",
                "capacity_card_1_image",
                "capacity_card_1_image_preview",
                # Карточка 2
                "capacity_card_2_title_uz",
                "capacity_card_2_title_ru",
                "capacity_card_2_title_en",
                "capacity_card_2_subtitle_uz",
                "capacity_card_2_subtitle_ru",
                "capacity_card_2_subtitle_en",
                "capacity_card_2_image",
                "capacity_card_2_image_preview",
                # Карточка 3
                "capacity_card_3_title_uz",
                "capacity_card_3_title_ru",
                "capacity_card_3_title_en",
                "capacity_card_3_subtitle_uz",
                "capacity_card_3_subtitle_ru",
                "capacity_card_3_subtitle_en",
                "capacity_card_3_image",
                "capacity_card_3_image_preview",
                # Карточка 4
                "capacity_card_4_title_uz",
                "capacity_card_4_title_ru",
                "capacity_card_4_title_en",
                "capacity_card_4_subtitle_uz",
                "capacity_card_4_subtitle_ru",
                "capacity_card_4_subtitle_en",
                "capacity_card_4_image",
                "capacity_card_4_image_preview",
            )
        }),
        # ========== СЕКЦИЯ 5: ПАРТНЕРСТВО ДЛЯ ДИЛЕРОВ ==========
        ("Партнерство для дилеров", {
            "fields": (
                "dealer_section_title_uz",
                "dealer_section_title_ru",
                "dealer_section_title_en",
                "dealer_title_uz",
                "dealer_title_ru",
                "dealer_title_en",
                # Карточка 1
                "dealer_card_1_title_uz",
                "dealer_card_1_title_ru",
                "dealer_card_1_title_en",
                "dealer_card_1_description_uz",
                "dealer_card_1_description_ru",
                "dealer_card_1_description_en",
                # Карточка 2
                "dealer_card_2_title_uz",
                "dealer_card_2_title_ru",
                "dealer_card_2_title_en",
                "dealer_card_2_description_uz",
                "dealer_card_2_description_ru",
                "dealer_card_2_description_en",
                # Карточка 3
                "dealer_card_3_title_uz",
                "dealer_card_3_title_ru",
                "dealer_card_3_title_en",
                "dealer_card_3_description_uz",
                "dealer_card_3_description_ru",
                "dealer_card_3_description_en",
            )
        }),
        # ========== СЕКЦИЯ 6: SEO ==========
        ("SEO", {
            "fields": (
                "meta_title_uz",
                "meta_title_ru",
                "meta_title_en",
                "meta_description_uz",
                "meta_description_ru",
                "meta_description_en",
                "meta_keywords_uz",
                "meta_keywords_ru",
                "meta_keywords_en",
                "og_title_uz",
                "og_title_ru",
                "og_title_en",
                "og_description_uz",
                "og_description_ru",
                "og_description_en",
                "og_image",
                "og_image_preview",
                "canonical_url_uz",
                "canonical_url_ru",
                "canonical_url_en",
            ),
            "description": "Настройки для поисковых систем и социальных сетей"
        }),
        # ========== НАСТРОЙКИ ==========
        ("Настройки", {
            "fields": ("is_published", "created_at", "update_at")
        }),
    )
    
    def changelist_view(self, request, extra_context=None):
        """Перенаправляем на форму редактирования, если есть запись, или на создание"""
        obj = AboutPage.objects.first()
        if obj:
            return HttpResponseRedirect(
                reverse('admin:catalog_aboutpage_change', args=[obj.pk])
            )
        return HttpResponseRedirect(
            reverse('admin:catalog_aboutpage_add')
        )
    
    def has_add_permission(self, request):
        """Разрешаем добавление только если нет записей"""
        return AboutPage.objects.count() == 0
    
    def has_delete_permission(self, request, obj=None):
        """Запрещаем удаление, так как должна быть только одна запись"""
        return False

    def about_section_title_preview(self, obj):
        """Превью названия секции для списка"""
        if obj:
            return obj.about_section_title_uz if hasattr(obj, 'about_section_title_uz') else obj.about_section_title
        return "-"
    about_section_title_preview.short_description = "Название секции"
    
    def about_image_1_preview(self, obj):
        """Превью первого изображения"""
        if obj and obj.about_image_1:
            return format_html(
                '<img src="{}" style="max-width: 300px; max-height: 200px; object-fit: cover; border-radius: 4px;"/>',
                obj.about_image_1.url
            )
        return "-"
    about_image_1_preview.short_description = "Превью изображения 1"
    
    def about_image_2_preview(self, obj):
        """Превью второго изображения"""
        if obj and obj.about_image_2:
            return format_html(
                '<img src="{}" style="max-width: 300px; max-height: 200px; object-fit: cover; border-radius: 4px;"/>',
                obj.about_image_2.url
            )
        return "-"
    about_image_2_preview.short_description = "Превью изображения 2"
    
    def capacity_card_1_image_preview(self, obj):
        """Превью изображения карточки 1"""
        if obj and obj.capacity_card_1_image:
            return format_html(
                '<img src="{}" style="max-width: 300px; max-height: 200px; object-fit: cover; border-radius: 4px;"/>',
                obj.capacity_card_1_image.url
            )
        return "-"
    capacity_card_1_image_preview.short_description = "Превью изображения карточки 1"
    
    def capacity_card_2_image_preview(self, obj):
        """Превью изображения карточки 2"""
        if obj and obj.capacity_card_2_image:
            return format_html(
                '<img src="{}" style="max-width: 300px; max-height: 200px; object-fit: cover; border-radius: 4px;"/>',
                obj.capacity_card_2_image.url
            )
        return "-"
    capacity_card_2_image_preview.short_description = "Превью изображения карточки 2"
    
    def capacity_card_3_image_preview(self, obj):
        """Превью изображения карточки 3"""
        if obj and obj.capacity_card_3_image:
            return format_html(
                '<img src="{}" style="max-width: 300px; max-height: 200px; object-fit: cover; border-radius: 4px;"/>',
                obj.capacity_card_3_image.url
            )
        return "-"
    capacity_card_3_image_preview.short_description = "Превью изображения карточки 3"
    
    def capacity_card_4_image_preview(self, obj):
        """Превью изображения карточки 4"""
        if obj and obj.capacity_card_4_image:
            return format_html(
                '<img src="{}" style="max-width: 300px; max-height: 200px; object-fit: cover; border-radius: 4px;"/>',
                obj.capacity_card_4_image.url
            )
        return "-"
    capacity_card_4_image_preview.short_description = "Превью изображения карточки 4"
    
    def og_image_preview(self, obj):
        """Превью OG изображения"""
        if obj and obj.og_image:
            return format_html(
                '<img src="{}" style="max-width: 300px; max-height: 200px; object-fit: cover; border-radius: 4px;"/>',
                obj.og_image.url
            )
        return "-"
    og_image_preview.short_description = "Превью OG изображения"


@admin.register(ContactPage)
class ContactPageAdmin(admin.ModelAdmin):
    """Админка для страницы контактов (singleton)"""
    list_display = ["page_title_preview", "phone", "email", "is_published", "created_at"]
    list_display_links = ["page_title_preview"]
    list_filter = ["is_published", "created_at"]
    search_fields = ["page_title_uz", "page_title_ru", "page_title_en", "address_uz", "phone", "email"]
    readonly_fields = ["og_image_preview", "created_at", "update_at"]
    
    fieldsets = (
        ("Заголовок страницы", {
            "fields": (
                "page_title_uz",
                "page_title_ru",
                "page_title_en",
            )
        }),
        ("Секция адреса", {
            "fields": (
                "address_label_uz",
                "address_label_ru",
                "address_label_en",
                "address_uz",
                "address_ru",
                "address_en"
            )
        }),
        ("Секция телефона", {
            "fields": (
                "phone_label_uz",
                "phone_label_ru",
                "phone_label_en",
                "phone"
            )
        }),
        ("Секция email", {
            "fields": (
                "email_label_uz",
                "email_label_ru",
                "email_label_en",
                "email"
            )
        }),
        ("Карта", {
            "fields": ("map_embed_url",),
            "description": "Вставьте ссылку на Google Maps для встраивания карты"
        }),
        ("Секция формы обратной связи", {
            "fields": (
                "form_title_uz",
                "form_title_ru",
                "form_title_en",
                "form_description_uz",
                "form_description_ru",
                "form_description_en"
            )
        }),
        ("Социальные сети", {
            "fields": ("facebook_url", "twitter_url", "linkedin_url", "instagram_url"),
            "classes": ("collapse",)
        }),
        ("SEO", {
            "fields": (
                "meta_title_uz",
                "meta_title_ru",
                "meta_title_en",
                "meta_description_uz",
                "meta_description_ru",
                "meta_description_en",
                "meta_keywords_uz",
                "meta_keywords_ru",
                "meta_keywords_en",
                "og_title_uz",
                "og_title_ru",
                "og_title_en",
                "og_description_uz",
                "og_description_ru",
                "og_description_en",
                "og_image",
                "og_image_preview",
                "canonical_url_uz",
                "canonical_url_ru",
                "canonical_url_en",
            ),
            "description": "Настройки для поисковых систем и социальных сетей"
        }),
        ("Настройки и даты", {
            "fields": ("is_published", "created_at", "update_at")
        }),
    )
    
    def changelist_view(self, request, extra_context=None):
        """Перенаправляем на форму редактирования, если есть запись, или на создание"""
        obj = ContactPage.objects.first()
        if obj:
            return HttpResponseRedirect(
                reverse('admin:catalog_contactpage_change', args=[obj.pk])
            )
        return HttpResponseRedirect(
            reverse('admin:catalog_contactpage_add')
        )
    
    def has_add_permission(self, request):
        """Разрешаем добавление только если нет записей"""
        return ContactPage.objects.count() == 0
    
    def has_delete_permission(self, request, obj=None):
        """Запрещаем удаление, так как должна быть только одна запись"""
        return False
    
    def page_title_preview(self, obj):
        """Превью заголовка для списка"""
        if obj:
            return obj.page_title_uz if hasattr(obj, 'page_title_uz') else obj.page_title
        return "-"
    page_title_preview.short_description = "Заголовок"
    
    def og_image_preview(self, obj):
        """Превью OG изображения"""
        if obj and obj.og_image:
            return format_html(
                '<img src="{}" style="max-width: 300px; max-height: 200px; object-fit: cover; border-radius: 4px;"/>',
                obj.og_image.url
            )
        return "-"
    og_image_preview.short_description = "Превью OG изображения"


class SalesPointInline(admin.StackedInline):
    """Inline для торговых точек региона"""
    model = SalesPoint
    extra = 0
    fields = [
        "name_uz",
        "name_ru",
        "name_en",
        "address_uz",
        "address_ru",
        "address_en",
        "location_uz",
        "location_ru",
        "location_en",
        "phone",
        "map_link",
        "order",
        "is_published"
    ]
    ordering = ["order"]


@admin.register(Region)
class RegionAdmin(admin.ModelAdmin):
    """Админка для регионов"""
    list_display = ["name", "slug", "sales_points_count", "order", "is_published"]
    list_display_links = ["name"]
    list_filter = ["is_published"]
    search_fields = ["name"]
    list_editable = ["order", "is_published"]
    inlines = [SalesPointInline]
    
    fieldsets = (
        ("Название региона", {
            "fields": (
                "name_uz",
                "name_ru",
                "name_en",
                "order"
            )
        }),
        ("Настройки", {
            "fields": ("is_published",)
        }),
    )
    
    def get_readonly_fields(self, request, obj=None):
        """Slug показывается только при редактировании существующего объекта"""
        readonly = []
        if obj:  # Если объект существует, показываем slug
            readonly.append("slug")
        return readonly
    
    def sales_points_count(self, obj):
        """Количество торговых точек в регионе"""
        return obj.sales_points.filter(is_published=True).count()
    sales_points_count.short_description = "Количество точек"


# SalesPoint управляется через inline в Region - не нужна отдельная админка


@admin.register(ContactFormSubmission)
class ContactFormSubmissionAdmin(admin.ModelAdmin):
    """Админка для заявок"""
    list_display = ["name", "phone", "email", "status", "created_at"]
    list_display_links = ["name"]
    list_filter = ["status", "created_at"]
    search_fields = ["name", "phone", "email", "message"]
    readonly_fields = ["created_at", "updated_at"]
    list_editable = ["status"]
    date_hierarchy = "created_at"
    
    fieldsets = (
        ("Информация от клиента", {
            "fields": ("name", "phone", "email", "message")
        }),
        ("Обработка", {
            "fields": ("status", "notes")
        }),
        ("Даты", {
            "fields": ("created_at", "updated_at")
        }),
    )
    
    def has_add_permission(self, request):
        """Запретить создание заявок вручную в админке"""
        return False


@admin.register(FAQ)
class FAQAdmin(admin.ModelAdmin):
    """Админка для FAQ"""
    list_display = ["question_short", "order", "is_published"]
    list_display_links = ["question_short"]
    list_filter = ["is_published", "created_at"]
    search_fields = ["question", "answer"]
    list_editable = ["order", "is_published"]
    
    fieldsets = (
        ("Вопрос", {
            "fields": (
                "question_uz",
                "question_ru",
                "question_en",
            )
        }),
        ("Ответ", {
            "fields": (
                "answer_uz",
                "answer_ru",
                "answer_en",
            )
        }),
        ("Настройки", {
            "fields": ("order", "is_published")
        }),
    )
    
    def question_short(self, obj):
        """Сокращенный вопрос"""
        return obj.question[:80] + "..." if len(obj.question) > 80 else obj.question
    question_short.short_description = "Вопрос"


@admin.register(GlobalSettings)
class GlobalSettingsAdmin(admin.ModelAdmin):
    """Админка для глобальных настроек (singleton)"""
    list_display = ["__str__", "is_published", "created_at"]
    list_display_links = ["__str__"]
    list_filter = ["is_published", "created_at"]
    readonly_fields = [
        "collection_cover_image_preview",
        "product_cover_image_preview",
        "created_at",
        "update_at"
    ]
    date_hierarchy = "created_at"
    
    fieldsets = (
        # ========== КОПИРАЙТ ==========
        ("Копирайт", {
            "fields": (
                "copyright_uz",
                "copyright_ru",
                "copyright_en",
            )
        }),
        # ========== МОДАЛЬНОЕ ОКНО ФОРМЫ ==========
        ("Модальное окно формы", {
            "fields": (
                "form_modal_title_uz",
                "form_modal_title_ru",
                "form_modal_title_en",
                "form_modal_text_uz",
                "form_modal_text_ru",
                "form_modal_text_en",
            )
        }),
        # ========== МОДАЛЬНОЕ ОКНО УСПЕХА ==========
        ("Модальное окно успеха", {
            "fields": (
                "success_modal_title_uz",
                "success_modal_title_ru",
                "success_modal_title_en",
                "success_modal_text_uz",
                "success_modal_text_ru",
                "success_modal_text_en",
            )
        }),
        # ========== КОНТАКТНАЯ ИНФОРМАЦИЯ ==========
        ("Контактная информация", {
            "fields": (
                "email",
                "phone",
                "address_uz",
                "address_ru",
                "address_en",
            )
        }),
        # ========== 3D ТУР ==========
        ("Tour 3D", {
            "fields": ("tour_3d_link",),
            "description": "Ссылка на 3D тур"
        }),
        # ========== ОБЛОЖКИ СТРАНИЦ ==========
        ("Обложки страниц", {
            "fields": (
                "collection_cover_image",
                "collection_cover_image_preview",
                "product_cover_image",
                "product_cover_image_preview",
            )
        }),
        # ========== SEO ПОЛЯ ==========
        ("SEO - Страница Коллекции", {
            "fields": (
                "collections_seo_title_uz",
                "collections_seo_title_ru",
                "collections_seo_title_en",
                "collections_seo_description_uz",
                "collections_seo_description_ru",
                "collections_seo_description_en",
            )
        }),
        ("SEO - Страница Новости", {
            "fields": (
                "news_seo_title_uz",
                "news_seo_title_ru",
                "news_seo_title_en",
                "news_seo_description_uz",
                "news_seo_description_ru",
                "news_seo_description_en",
            )
        }),
        ("SEO - Страница Галерея", {
            "fields": (
                "gallery_seo_title_uz",
                "gallery_seo_title_ru",
                "gallery_seo_title_en",
                "gallery_seo_description_uz",
                "gallery_seo_description_ru",
                "gallery_seo_description_en",
            )
        }),
        # ========== НАСТРОЙКИ ==========
        ("Настройки", {
            "fields": ("is_published", "created_at", "update_at"),
        }),
    )
    
    def changelist_view(self, request, extra_context=None):
        """Перенаправляем на форму редактирования, если есть запись, или на создание"""
        obj = GlobalSettings.objects.first()
        if obj:
            return HttpResponseRedirect(
                reverse('admin:catalog_globalsettings_change', args=[obj.pk])
            )
        return HttpResponseRedirect(
            reverse('admin:catalog_globalsettings_add')
        )
    
    def collection_cover_image_preview(self, obj):
        """Превью обложки страницы коллекции"""
        if obj and obj.collection_cover_image:
            return format_html(
                '<img src="{}" style="max-width: 300px; max-height: 200px; object-fit: cover; border-radius: 4px;"/>',
                obj.collection_cover_image.url
            )
        return "-"
    collection_cover_image_preview.short_description = "Превью обложки коллекции"
    
    def product_cover_image_preview(self, obj):
        """Превью обложки страницы продуктов"""
        if obj and obj.product_cover_image:
            return format_html(
                '<img src="{}" style="max-width: 300px; max-height: 200px; object-fit: cover; border-radius: 4px;"/>',
                obj.product_cover_image.url
            )
        return "-"
    product_cover_image_preview.short_description = "Превью обложки продуктов"


@admin.register(InstagramPost)
class InstagramPostAdmin(admin.ModelAdmin):
    """Админка для постов Instagram"""
    list_display = [
        "thumbnail_preview",
        "instagram_id",
        "post_type",
        "caption_preview",
        "like_count",
        "comments_count",
        "timestamp",
        "is_published",
        "created_at",
    ]
    list_display_links = ["thumbnail_preview", "instagram_id"]
    list_filter = ["post_type", "is_published", "timestamp", "created_at"]
    search_fields = ["instagram_id", "caption"]
    readonly_fields = [
        "instagram_id",
        "post_type",
        "caption",
        "permalink",
        "thumbnail_url",
        "media_url",
        "like_count",
        "comments_count",
        "timestamp",
        "created_at",
        "updated_at",
        "thumbnail_preview",
        "media_preview",
    ]
    date_hierarchy = "timestamp"
    fieldsets = (
        ("Основная информация", {
            "fields": (
                "instagram_id",
                "post_type",
                "caption",
                "permalink",
                "timestamp",
            )
        }),
        ("Медиа", {
            "fields": (
                "thumbnail_url",
                "thumbnail_preview",
                "media_url",
                "media_preview",
            )
        }),
        ("Метрики", {
            "fields": (
                "like_count",
                "comments_count",
            )
        }),
        ("Настройки", {
            "fields": (
                "is_published",
                "created_at",
                "updated_at",
            )
        }),
    )
    
    def thumbnail_preview(self, obj):
        """Превью миниатюры"""
        if obj.thumbnail_url:
            return format_html(
                '<img src="{}" style="max-width: 100px; max-height: 100px;" />',
                obj.thumbnail_url
            )
        return "-"
    thumbnail_preview.short_description = "Миниатюра"
    
    def media_preview(self, obj):
        """Превью медиа"""
        if obj.media_url:
            if obj.post_type == 'VIDEO':
                return format_html(
                    '<video src="{}" controls style="max-width: 300px; max-height: 300px;" />',
                    obj.media_url
                )
            else:
                return format_html(
                    '<img src="{}" style="max-width: 300px; max-height: 300px;" />',
                    obj.media_url
                )
        return "-"
    media_preview.short_description = "Медиа"
    
    def caption_preview(self, obj):
        """Превью подписи (первые 50 символов)"""
        if obj.caption:
            return obj.caption[:50] + "..." if len(obj.caption) > 50 else obj.caption
        return "-"
    caption_preview.short_description = "Подпись"


# AdvantageCard управляется через inline на главной странице - не нужна отдельная админка