from django.contrib import admin
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.utils.html import format_html
from django.utils.safestring import mark_safe

from apps.catalog.models import (
    AboutPage,
    AdvantageCard,
    Carpet,
    CarpetImage,
    Collection,
    Color,
    CompanyHistory,
    ContactFormSubmission,
    ContactPage,
    DealerAdvantage,
    FAQ,
    Gallery,
    HomePage,
    MainGallery,
    News,
    NewsContentBlock,
    NewsImage,
    ProductionCapacity,
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
    """Inline для изображений блока контента"""
    model = NewsImage
    extra = 0
    max_num = 3
    fields = [
        "image",
        "caption_uz",
        "caption_ru",
        "caption_en",
        "order"
    ]
    ordering = ["order"]
    
    def get_formset(self, request, obj=None, **kwargs):
        """Ограничить максимум 3 изображения"""
        formset = super().get_formset(request, obj, **kwargs)
        return formset


class NewsContentBlockInline(admin.StackedInline):
    """Inline для блоков контента новости"""
    model = NewsContentBlock
    extra = 0
    fields = [
        "content_type",
        "order",
        "title_uz",
        "title_ru",
        "title_en",
        "text_content_uz",
        "text_content_ru",
        "text_content_en",
        "images_help"
    ]
    readonly_fields = ["images_help"]
    ordering = ["order"]
    
    def images_help(self, obj):
        """Помощь по добавлению изображений"""
        if obj and obj.pk and obj.content_type == 'images':
            url = f'/admin/catalog/newscontentblock/{obj.pk}/change/'
            return format_html(
                '<a href="{}" target="_blank" style="display: inline-block; padding: 8px 12px; background: #417690; color: white; text-decoration: none; border-radius: 4px;">➕ Добавить/редактировать изображения для этого блока</a>',
                url
            )
        elif obj and obj.pk:
            return format_html('<p style="color: #666;">Измените тип блока на "Блок изображений" чтобы добавить изображения</p>')
        return format_html('<p style="color: #666;">Сохраните блок сначала, чтобы добавить изображения</p>')
    images_help.short_description = "Изображения"
    
    class Media:
        js = (
            'https://cdn.ckeditor.com/4.25.1-lts/standard/ckeditor.js',
            'js/ckeditor_init.js',
        )


@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    """Админка для новостей с динамическими блоками контента"""
    list_display = ["cover_image_preview", "title", "slug", "is_published", "created_at"]
    list_display_links = ["title"]
    list_filter = ["is_published", "created_at"]
    search_fields = ["title", "description"]
    readonly_fields = ["cover_image_preview", "created_at", "update_at"]
    date_hierarchy = "created_at"
    inlines = [NewsContentBlockInline]
    
    fieldsets = (
        ("Основная информация", {
            "fields": ("title_uz", "title_ru", "title_en")
        }),
        ("Описание", {
            "fields": ("description_uz", "description_ru", "description_en")
        }),
        ("Главное изображение", {
            "fields": ("cover_image", "cover_image_preview"),
            "description": "Изображение для превью новости в списке"
        }),
        ("Настройки", {
            "fields": ("is_published",)
        }),
        ("Даты", {
            "fields": ("created_at", "update_at")
        }),
    )
    
    def get_readonly_fields(self, request, obj=None):
        """Slug показывается только при редактировании существующего объекта"""
        readonly = list(self.readonly_fields)
        if obj:  # Если объект существует, показываем slug
            readonly.append("slug")
        return readonly

    def cover_image_preview(self, obj):
        """Превью главного изображения"""
        if obj.cover_image:
            return format_html(
                '<img src="{}" style="max-width: 150px; max-height: 150px; object-fit: cover; border-radius: 4px;"/>',
                obj.cover_image.url
            )
        return "-"
    cover_image_preview.short_description = "Превью"


# NewsContentBlock - скрытая админка для редактирования изображений
class NewsContentBlockAdmin(admin.ModelAdmin):
    """Админка для блоков контента (для редактирования изображений)"""
    list_display = ["news", "content_type", "order"]
    list_filter = ["content_type", "news"]
    search_fields = ["news__title"]
    inlines = [NewsImageInline]
    
    fieldsets = (
        ("Основная информация", {
            "fields": ("news", "content_type", "order")
        }),
        ("Текстовое содержание", {
            "fields": (
                "text_content",
                "text_content_ru",
                "text_content_en"
            ),
            "description": "Заполняется только для текстовых блоков"
        }),
    )
    
    class Media:
        js = (
            'https://cdn.ckeditor.com/4.25.1-lts/standard/ckeditor.js',
            'js/ckeditor_init.js',
        )
    
    def has_module_permission(self, request):
        """Скрыть из списка приложений в админке"""
        return False

admin.site.register(NewsContentBlock, NewsContentBlockAdmin)


@admin.register(Gallery)
class GalleryAdmin(admin.ModelAdmin):
    """Админка для галереи"""
    list_display = ["image_preview", "title", "order", "is_published", "created_at"]
    list_display_links = ["title", "image_preview"]
    list_filter = ["is_published", "created_at"]
    search_fields = ["title"]
    readonly_fields = ["image_preview", "created_at"]
    list_editable = ["order", "is_published"]
    fieldsets = (
        ("Основная информация", {
            "fields": ("title", "order")
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


@admin.register(HomePage)
class HomePageAdmin(admin.ModelAdmin):
    """Админка для главной страницы с табами"""
    list_display = ["banner_title_preview", "is_published", "created_at"]
    list_display_links = ["banner_title_preview"]
    list_filter = ["is_published", "created_at"]
    search_fields = ["banner_title_uz", "banner_title_ru", "banner_title_en"]
    readonly_fields = [
        "banner_image_preview",
        "banner_showroom_image_preview",
        "about_image_1_preview",
        "about_image_2_preview",
        "about_image_3_preview",
        "showroom_image_preview",
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
                "banner_showroom_link_uz",
                "banner_showroom_link_ru",
                "banner_showroom_link_en",
                "banner_showroom_image",
                "banner_showroom_image_preview",
            )
        }),
        # ========== ТАБ 2: О НАС ==========
        ("О нас", {
            "fields": (
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
                "about_image_1",
                "about_image_1_preview",
                "about_image_2",
                "about_image_2_preview",
                "about_image_3",
                "about_image_3_preview",
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
                "showroom_link_uz",
                "showroom_link_ru",
                "showroom_link_en",
            )
        }),
        # ========== ТАБ 4: ПРЕИМУЩЕСТВА ==========
        ("Преимущества", {
            "fields": (
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
                "cta_contact_link",
                "cta_dealer_link",
            )
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
    
    def about_image_1_preview(self, obj):
        """Превью первого изображения секции 'О нас'"""
        if obj and obj.about_image_1:
            return format_html(
                '<img src="{}" style="max-width: 300px; max-height: 200px; object-fit: cover; border-radius: 4px;"/>',
                obj.about_image_1.url
            )
        return "-"
    about_image_1_preview.short_description = "Превью изображения 1"
    
    def about_image_2_preview(self, obj):
        """Превью второго изображения секции 'О нас'"""
        if obj and obj.about_image_2:
            return format_html(
                '<img src="{}" style="max-width: 300px; max-height: 200px; object-fit: cover; border-radius: 4px;"/>',
                obj.about_image_2.url
            )
        return "-"
    about_image_2_preview.short_description = "Превью изображения 2"
    
    def about_image_3_preview(self, obj):
        """Превью третьего изображения секции 'О нас'"""
        if obj and obj.about_image_3:
            return format_html(
                '<img src="{}" style="max-width: 300px; max-height: 200px; object-fit: cover; border-radius: 4px;"/>',
                obj.about_image_3.url
            )
        return "-"
    about_image_3_preview.short_description = "Превью изображения 3"
    
    def showroom_image_preview(self, obj):
        """Превью изображения секции шоурума"""
        if obj and obj.showroom_image:
            return format_html(
                '<img src="{}" style="max-width: 300px; max-height: 200px; object-fit: cover; border-radius: 4px;"/>',
                obj.showroom_image.url
            )
        return "-"
    showroom_image_preview.short_description = "Превью изображения шоурума"


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
        "order",
        "year",
        "title_uz",
        "title_ru",
        "title_en",
        "description_uz",
        "description_ru",
        "description_en",
        "image"
    ]
    ordering = ["order", "year"]


class ProductionCapacityInline(admin.StackedInline):
    """Inline для объемов производства"""
    model = ProductionCapacity
    extra = 1
    fields = [
        "order",
        "year",
        "capacity_uz",
        "capacity_ru",
        "capacity_en",
        "description_uz",
        "description_ru",
        "description_en",
        "image"
    ]
    ordering = ["order", "year"]


class DealerAdvantageInline(admin.StackedInline):
    """Inline для преимуществ дилеров"""
    model = DealerAdvantage
    extra = 1
    fields = [
        "order",
        "title_uz",
        "title_ru",
        "title_en",
        "description_uz",
        "description_ru",
        "description_en",
        "is_published"
    ]
    ordering = ["order"]


@admin.register(AboutPage)
class AboutPageAdmin(admin.ModelAdmin):
    """Админка для страницы о компании"""
    list_display = ["main_image_preview", "company_title", "is_published", "created_at"]
    list_display_links = ["company_title"]
    list_filter = ["is_published", "created_at"]
    search_fields = ["company_title", "company_description"]
    readonly_fields = ["main_image_preview", "showroom_image_preview", "created_at", "update_at"]
    date_hierarchy = "created_at"
    inlines = [ProductionStepInline, CompanyHistoryInline, ProductionCapacityInline, DealerAdvantageInline]
    fieldsets = (
        ("Описание компании", {
            "fields": (
                "company_title_uz",
                "company_title_ru",
                "company_title_en",
                "company_subtitle_uz",
                "company_subtitle_ru",
                "company_subtitle_en",
                "company_description_uz",
                "company_description_ru",
                "company_description_en",
                "main_image",
                "main_image_preview",
            )
        }),
        ("Секция производства - заголовок", {
            "fields": (
                "production_section_title_uz",
                "production_section_title_ru",
                "production_section_title_en",
            )
        }),
        ("Секция истории - заголовок", {
            "fields": (
                "history_section_title_uz",
                "history_section_title_ru",
                "history_section_title_en",
            )
        }),
        ("Секция объемов производства - заголовок", {
            "fields": (
                "capacity_section_title_uz",
                "capacity_section_title_ru",
                "capacity_section_title_en",
            )
        }),
        ("Секция дилеров - заголовок", {
            "fields": (
                "dealer_section_title_uz",
                "dealer_section_title_ru",
                "dealer_section_title_en",
            )
        }),
        ("Секция шоурума", {
            "fields": (
                "showroom_button_text_uz",
                "showroom_button_text_ru",
                "showroom_button_text_en",
                "showroom_image",
                "showroom_image_preview",
            )
        }),
        ("Настройки и даты", {
            "fields": ("is_published", "created_at", "update_at")
        }),
    )

    def main_image_preview(self, obj):
        """Превью главного изображения"""
        if obj.main_image:
            return format_html(
                '<img src="{}" style="max-width: 300px; max-height: 200px; object-fit: cover; border-radius: 4px;"/>',
                obj.main_image.url
            )
        return "-"
    main_image_preview.short_description = "Превью главного изображения"

    def showroom_image_preview(self, obj):
        """Превью изображения шоурума"""
        if obj.showroom_image:
            return format_html(
                '<img src="{}" style="max-width: 300px; max-height: 200px; object-fit: cover; border-radius: 4px;"/>',
                obj.showroom_image.url
            )
        return "-"
    showroom_image_preview.short_description = "Превью изображения шоурума"


@admin.register(ContactPage)
class ContactPageAdmin(admin.ModelAdmin):
    """Админка для страницы контактов"""
    list_display = ["page_title", "phone", "email", "is_published", "created_at"]
    list_display_links = ["page_title"]
    list_filter = ["is_published", "created_at"]
    search_fields = ["page_title", "address", "phone", "email"]
    readonly_fields = ["created_at", "update_at"]
    
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
        ("Настройки и даты", {
            "fields": ("is_published", "created_at", "update_at")
        }),
    )


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


# AdvantageCard управляется через inline на главной странице - не нужна отдельная админка