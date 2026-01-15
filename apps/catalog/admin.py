from django.contrib import admin
from django.utils.html import format_html
from django.utils.safestring import mark_safe

from apps.catalog.models import (
    AboutPage,
    AdvantageCard,
    Carpet,
    Collection,
    Color,
    ContactFormSubmission,
    ContactPage,
    DealerAdvantage,
    FAQ,
    Gallery,
    HomePage,
    News,
    NewsContentBlock,
    NewsImage,
    Region,
    Room,
    SalesPoint,
    Style,
    TypeCarpetCollection,
)


@admin.register(TypeCarpetCollection)
class TypeCarpetCollectionAdmin(admin.ModelAdmin):
    """Админка для типов ковров"""
    list_display = ["image_preview", "type", "slug"]
    list_display_links = ["type"]
    search_fields = ["type", "description"]
    prepopulated_fields = {"slug": ("type",)}
    readonly_fields = ["image_preview"]
    fieldsets = (
        ("Основная информация", {
            "fields": ("type", "slug", "description")
        }),
        ("Изображение", {
            "fields": ("image", "image_preview")
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


@admin.register(Collection)
class CollectionAdmin(admin.ModelAdmin):
    """Админка для коллекций"""
    list_display = ["image_preview", "name", "type", "is_published", "is_new", "carpets_count", "created_at"]
    list_display_links = ["name"]
    list_filter = ["is_published", "is_new", "type", "created_at"]
    search_fields = ["name", "description"]
    prepopulated_fields = {"slug": ("name",)}
    readonly_fields = ["image_preview", "created_at", "update_at", "carpets_count"]
    date_hierarchy = "created_at"
    fieldsets = (
        ("Основная информация", {
            "fields": ("name", "slug", "type", "description")
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


class CarpetImageInline(admin.TabularInline):
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
                "material",
                "density",
                "base",
                "pile_height",
                "yarn_composition",
                "weight"
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


class NewsImageInline(admin.TabularInline):
    """Inline для изображений блока контента"""
    model = NewsImage
    extra = 0
    max_num = 3
    fields = ["image", "caption", "caption_ru", "caption_en", "order"]
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
        "text_content", "text_content_ru", "text_content_en",
    ]
    ordering = ["order"]
    
    class Media:
        js = (
            'https://cdn.ckeditor.com/4.22.1/standard/ckeditor.js',
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
            "fields": ("title", "title_ru", "title_en", "slug")
        }),
        ("Описание", {
            "fields": ("description", "description_ru", "description_en")
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


@admin.register(NewsContentBlock)
class NewsContentBlockAdmin(admin.ModelAdmin):
    """Админка для блоков контента (для добавления изображений)"""
    list_display = ["news", "content_type", "order"]
    list_filter = ["content_type", "news"]
    search_fields = ["news__title"]
    inlines = [NewsImageInline]
    
    fieldsets = (
        ("Основная информация", {
            "fields": ("news", "content_type", "order")
        }),
        ("Текстовое содержание", {
            "fields": ("text_content", "text_content_ru", "text_content_en"),
            "description": "Заполняется только для текстовых блоков"
        }),
    )
    
    class Media:
        js = (
            'https://cdn.ckeditor.com/4.22.1/standard/ckeditor.js',
            'js/ckeditor_init.js',
        )


@admin.register(Gallery)
class GalleryAdmin(admin.ModelAdmin):
    """Админка для галереи"""
    list_display = ["image_preview", "title", "order", "is_published", "created_at"]
    list_display_links = ["title"]
    list_filter = ["is_published", "created_at"]
    search_fields = ["title", "description"]
    readonly_fields = ["image_preview", "created_at"]
    list_editable = ["order", "is_published"]
    fieldsets = (
        ("Основная информация", {
            "fields": ("title", "description", "order")
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
        ("Основная информация", {
            "fields": ("title", "title_ru", "title_en", "description", "description_ru", "description_en")
        }),
        ("Изображение", {
            "fields": ("image", "image_preview")
        }),
        ("Ссылки", {
            "fields": (
                "collection_link", "collection_link_ru", "collection_link_en",
                "showroom_title", "showroom_title_ru", "showroom_title_en",
                "showroom_link", "showroom_link_ru", "showroom_link_en"
            )
        }),
        ("Настройки", {
            "fields": ("is_published",)
        }),
        ("Даты", {
            "fields": ("created_at", "update_at")
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


class DealerAdvantageInline(admin.TabularInline):
    """Inline для преимуществ дилеров"""
    model = DealerAdvantage
    extra = 1
    fields = [
        "order",
        "title", "title_ru", "title_en",
        "description", "description_ru", "description_en",
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
    readonly_fields = ["main_image_preview", "showroom_image_preview", "created_at", "update_at", "json_help"]
    date_hierarchy = "created_at"
    inlines = [DealerAdvantageInline]
    fieldsets = (
        ("Основная информация", {
            "fields": (
                "company_title", "company_title_ru", "company_title_en",
                "company_subtitle", "company_subtitle_ru", "company_subtitle_en",
                "company_description", "company_description_ru", "company_description_en"
            )
        }),
        ("Изображения", {
            "fields": (
                "main_image", "main_image_preview",
                "showroom_image", "showroom_image_preview"
            )
        }),
        ("Заголовки секций", {
            "fields": (
                "production_section_title", "production_section_title_ru", "production_section_title_en",
                "history_section_title", "history_section_title_ru", "history_section_title_en",
                "capacity_section_title", "capacity_section_title_ru", "capacity_section_title_en",
                "dealer_section_title", "dealer_section_title_ru", "dealer_section_title_en",
                "showroom_button_text", "showroom_button_text_ru", "showroom_button_text_en"
            )
        }),
        ("Этапы производства", {
            "fields": ("production_steps",),
            "description": "Формат: [{\"order\": 1, \"title\": \"...\", \"title_ru\": \"...\", \"title_en\": \"...\", \"description\": \"...\", \"description_ru\": \"...\", \"description_en\": \"...\", \"image\": \"url\"}]"
        }),
        ("История компании", {
            "fields": ("company_history",),
            "description": "Формат: [{\"year\": 2005, \"title\": \"...\", \"title_ru\": \"...\", \"title_en\": \"...\", \"description\": \"...\", \"description_ru\": \"...\", \"description_en\": \"...\", \"image\": \"url\"}]"
        }),
        ("Объемы производства", {
            "fields": ("production_capacity",),
            "description": "Формат: [{\"year\": 2005, \"capacity\": \"...\", \"capacity_ru\": \"...\", \"capacity_en\": \"...\", \"description\": \"...\", \"description_ru\": \"...\", \"description_en\": \"...\", \"image\": \"url\"}]"
        }),
        ("Справка по JSON", {
            "fields": ("json_help",),
            "classes": ("collapse",),
        }),
        ("Настройки", {
            "fields": ("is_published",)
        }),
        ("Даты", {
            "fields": ("created_at", "update_at")
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

    def json_help(self, obj):
        """Справка по формату JSON полей"""
        return format_html(
            """
            <div style="padding: 15px; background: #f8f9fa; border-radius: 4px; font-family: monospace;">
                <h3 style="margin-top: 0;">Формат JSON полей:</h3>
                
                <h4>1. Этапы производства (production_steps):</h4>
                <pre style="background: white; padding: 10px; border-radius: 4px;">{{
  "order": 1,
  "title": "Iplarni tayyorlash va bo'yash",
  "title_ru": "Подготовка и окраска нитей",
  "title_en": "Preparation and dyeing of threads",
  "description": "Ranglarning yorqinligi va...",
  "description_ru": "Яркость красок и...",
  "description_en": "Brightness of colors and...",
  "image": "/media/photos/about/production/step1.jpg"
}}</pre>
                
                <h4>2. История компании (company_history):</h4>
                <pre style="background: white; padding: 10px; border-radius: 4px;">{{
  "year": 2007,
  "title": "Kengayish davri",
  "title_ru": "Период расширения",
  "title_en": "Expansion period",
  "description": "Kompaniya asoschisi...",
  "description_ru": "Основатель компании...",
  "description_en": "Company founder...",
  "image": "/media/photos/about/history/2007.jpg"
}}</pre>

                <h4>3. Объемы производства (production_capacity):</h4>
                <pre style="background: white; padding: 10px; border-radius: 4px;">{{
  "year": 2024,
  "capacity": "100 000 000 mln. m²",
  "capacity_ru": "100 000 000 млн. м²",
  "capacity_en": "100,000,000 million m²",
  "description": "...",
  "description_ru": "...",
  "description_en": "...",
  "image": "/media/photos/about/capacity/2024.jpg"
}}</pre>

                <p style="margin-top: 15px; color: #666;">
                    <strong>Примечание:</strong> Каждое поле должно быть массивом объектов. 
                    Для изображений используйте относительные пути от MEDIA_ROOT.
                </p>
                
                <h4>4. Преимущества для дилеров:</h4>
                <p style="color: #666;">
                    Преимущества для дилеров редактируются через форму ниже (Inline Admin).
                    Вы можете добавлять, редактировать и удалять преимущества прямо на этой странице.
                </p>
            </div>
            """
        )
    json_help.short_description = "Справка по JSON полям"


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
            "fields": ("page_title", "page_title_ru", "page_title_en")
        }),
        ("Адрес", {
            "fields": (
                "address_label", "address_label_ru", "address_label_en",
                "address", "address_ru", "address_en"
            )
        }),
        ("Телефон", {
            "fields": (
                "phone_label", "phone_label_ru", "phone_label_en",
                "phone"
            )
        }),
        ("Email", {
            "fields": (
                "email_label", "email_label_ru", "email_label_en",
                "email"
            )
        }),
        ("Карта", {
            "fields": ("map_embed_url",),
            "description": "Вставьте ссылку на Google Maps для встраивания карты"
        }),
        ("Форма обратной связи", {
            "fields": (
                "form_title", "form_title_ru", "form_title_en",
                "form_description", "form_description_ru", "form_description_en"
            )
        }),
        ("Социальные сети", {
            "fields": ("facebook_url", "twitter_url", "linkedin_url", "instagram_url"),
            "classes": ("collapse",)
        }),
        ("Настройки", {
            "fields": ("is_published",)
        }),
        ("Даты", {
            "fields": ("created_at", "update_at")
        }),
    )


class SalesPointInline(admin.TabularInline):
    """Inline для торговых точек региона"""
    model = SalesPoint
    extra = 0
    fields = [
        "name", "name_ru", "name_en",
        "point_type",
        "address", "location",
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
        ("Основная информация", {
            "fields": (
                "name", "name_ru", "name_en",
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


@admin.register(SalesPoint)
class SalesPointAdmin(admin.ModelAdmin):
    """Админка для торговых точек"""
    list_display = ["name", "region", "point_type", "phone", "order", "is_published"]
    list_display_links = ["name"]
    list_filter = ["region", "point_type", "is_published"]
    search_fields = ["name", "address", "location", "phone"]
    list_editable = ["order", "is_published"]
    
    fieldsets = (
        ("Основная информация", {
            "fields": (
                "region",
                "name", "name_ru", "name_en",
                "point_type"
            )
        }),
        ("Адрес", {
            "fields": (
                "address", "address_ru", "address_en",
                "location", "location_ru", "location_en"
            )
        }),
        ("Контакты", {
            "fields": ("phone",)
        }),
        ("Карта", {
            "fields": ("map_link",),
            "description": "Ссылка на Google Maps или Яндекс.Карты"
        }),
        ("Настройки", {
            "fields": ("order", "is_published")
        }),
    )


@admin.register(ContactFormSubmission)
class ContactFormSubmissionAdmin(admin.ModelAdmin):
    """Админка для заявок"""
    list_display = ["name", "phone", "status", "created_at"]
    list_display_links = ["name"]
    list_filter = ["status", "created_at"]
    search_fields = ["name", "phone", "message"]
    readonly_fields = ["created_at", "updated_at"]
    list_editable = ["status"]
    date_hierarchy = "created_at"
    
    fieldsets = (
        ("Информация от клиента", {
            "fields": ("name", "phone", "message")
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
            "fields": ("question", "question_ru", "question_en")
        }),
        ("Ответ", {
            "fields": ("answer", "answer_ru", "answer_en")
        }),
        ("Настройки", {
            "fields": ("order", "is_published")
        }),
    )
    
    def question_short(self, obj):
        """Сокращенный вопрос"""
        return obj.question[:80] + "..." if len(obj.question) > 80 else obj.question
    question_short.short_description = "Вопрос"


@admin.register(AdvantageCard)
class AdvantageCardAdmin(admin.ModelAdmin):
    """Админка для карточек преимуществ"""
    list_display = ["order", "title", "has_icon", "is_published"]
    list_display_links = ["title"]
    list_filter = ["is_published"]
    search_fields = ["title", "description"]
    list_editable = ["order", "is_published"]
    
    fieldsets = (
        ("Основная информация", {
            "fields": (
                "order",
                "title", "title_ru", "title_en",
                "description", "description_ru", "description_en"
            )
        }),
        ("SVG Иконка", {
            "fields": ("svg_icon",),
            "description": "Вставьте код SVG для иконки (опционально)"
        }),
        ("Настройки", {
            "fields": ("is_published",)
        }),
    )
    
    def has_icon(self, obj):
        """Есть ли иконка"""
        return bool(obj.svg_icon)
    has_icon.boolean = True
    has_icon.short_description = "Иконка"