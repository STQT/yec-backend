from django.contrib import admin
from django.utils.html import format_html
from django.utils.safestring import mark_safe

from apps.catalog.models import (
    AboutPage,
    AdvantageCard,
    Carpet,
    Collection,
    Color,
    CompanyHistory,
    ContactFormSubmission,
    ContactPage,
    DealerAdvantage,
    FAQ,
    Gallery,
    HomePage,
    News,
    NewsContentBlock,
    NewsImage,
    PointType,
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
    list_display = ["image_preview", "name", "is_published", "is_new", "carpets_count", "created_at"]
    list_display_links = ["name"]
    list_filter = ["is_published", "is_new", "created_at"]
    search_fields = ["name", "description"]
    prepopulated_fields = {"slug": ("name",)}
    readonly_fields = ["image_preview", "created_at", "update_at", "carpets_count"]
    date_hierarchy = "created_at"
    fieldsets = (
        ("Основная информация", {
            "fields": ("name", "slug", "description")
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
    prepopulated_fields = {"slug": ("name",)}
    readonly_fields = ["carpets_count"]

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
    prepopulated_fields = {"slug": ("name",)}
    readonly_fields = ["carpets_count"]

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
    prepopulated_fields = {"slug": ("name",)}
    readonly_fields = ["color_preview", "carpets_count"]

    def color_preview(self, obj):
        """Превью цвета"""
        if obj.hex_code:
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


@admin.register(PointType)
class PointTypeAdmin(admin.ModelAdmin):
    """Админка для типов точек"""
    list_display = ["name", "slug", "order", "is_published", "sales_points_count"]
    list_display_links = ["name"]
    list_filter = ["is_published"]
    search_fields = ["name"]
    prepopulated_fields = {"slug": ("name",)}
    list_editable = ["order", "is_published"]
    readonly_fields = ["sales_points_count"]
    
    def sales_points_count(self, obj):
        """Количество торговых точек с типом"""
        return obj.sales_points.count()
    sales_points_count.short_description = "Количество точек"
    
    fieldsets = (
        ("Название типа точки", {
            "fields": (
                "name_uz",
                "name_ru",
                "name_en",
                "slug",
                "order",
                "is_published"
            )
        }),
    )


class CarpetImageInline(admin.StackedInline):
    """Inline для дополнительных изображений ковра (если понадобится в будущем)"""
    model = Carpet
    extra = 0
    fields = ["photo", "code"]
    readonly_fields = ["photo"]


@admin.register(Carpet)
class CarpetAdmin(admin.ModelAdmin):
    """Админка для ковров"""
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
    list_display_links = ["code"]
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
            "fields": ("code", "collection", "roll")
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
    list_display = ["cover_image_preview", "title", "is_published", "created_at"]
    list_display_links = ["title"]
    list_filter = ["is_published", "created_at"]
    search_fields = ["title", "description"]
    prepopulated_fields = {"slug": ("title",)}
    readonly_fields = ["cover_image_preview", "created_at", "update_at"]
    date_hierarchy = "created_at"
    inlines = [NewsContentBlockInline]
    
    fieldsets = (
        ("Основная информация", {
            "fields": ("title_uz", "title_ru", "title_en", "slug")
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


@admin.register(HomePage)
class HomePageAdmin(admin.ModelAdmin):
    """Админка для главной страницы"""
    list_display = ["image_preview", "title", "is_published", "created_at"]
    list_display_links = ["title"]
    list_filter = ["is_published", "created_at"]
    search_fields = ["title", "description"]
    readonly_fields = ["image_preview", "created_at", "update_at"]
    date_hierarchy = "created_at"
    fieldsets = (
        ("Заголовок и описание", {
            "fields": (
                "title_uz",
                "title_ru",
                "title_en",
                "description_uz",
                "description_ru",
                "description_en"
            )
        }),
        ("Секция коллекций", {
            "fields": (
                "collection_link_uz",
                "collection_link_ru",
                "collection_link_en",
            )
        }),
        ("Секция шоурума", {
            "fields": (
                "showroom_title_uz",
                "showroom_title_ru",
                "showroom_title_en",
                "showroom_link_uz",
                "showroom_link_ru",
                "showroom_link_en"
            )
        }),
        ("Медиафайлы", {
            "fields": ("image", "video", "image_preview")
        }),
        ("Настройки и даты", {
            "fields": ("is_published", "created_at", "update_at")
        }),
    )

    def image_preview(self, obj):
        """Превью изображения"""
        if obj.image:
            return format_html(
                '<img src="{}" style="max-width: 300px; max-height: 200px; object-fit: cover; border-radius: 4px;"/>',
                obj.image.url
            )
        return "-"
    image_preview.short_description = "Превью"


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
        "point_type",
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
    prepopulated_fields = {"slug": ("name",)}
    list_editable = ["order", "is_published"]
    inlines = [SalesPointInline]
    
    fieldsets = (
        ("Название региона", {
            "fields": (
                "name_uz",
                "name_ru",
                "name_en",
                "slug",
                "order"
            )
        }),
        ("Настройки", {
            "fields": ("is_published",)
        }),
    )
    
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