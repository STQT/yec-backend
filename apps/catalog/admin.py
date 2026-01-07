from django.contrib import admin
from django.utils.html import format_html
from django.utils.safestring import mark_safe

from apps.catalog.models import (
    Carpet,
    Collection,
    Color,
    Gallery,
    News,
    Room,
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


@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    """Админка для новостей"""
    list_display = ["image_preview", "title", "is_published", "created_at"]
    list_display_links = ["title"]
    list_filter = ["is_published", "created_at"]
    search_fields = ["title", "description", "content"]
    prepopulated_fields = {"slug": ("title",)}
    readonly_fields = ["image_preview", "created_at", "update_at"]
    date_hierarchy = "created_at"
    fieldsets = (
        ("Основная информация", {
            "fields": ("title", "slug", "description", "content")
        }),
        ("Изображение", {
            "fields": ("image", "image_preview")
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
                '<img src="{}" style="max-width: 150px; max-height: 150px; object-fit: cover; border-radius: 4px;"/>',
                obj.image.url
            )
        return "-"
    image_preview.short_description = "Превью"


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