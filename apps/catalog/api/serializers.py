from rest_framework import serializers

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


class ImageFieldSerializer(serializers.ImageField):
    """Кастомное поле для изображений с полным URL"""
    def to_representation(self, value):
        if not value:
            return None
        request = self.context.get("request")
        if request:
            return request.build_absolute_uri(value.url)
        return value.url


class TypeCarpetCollectionSerializer(serializers.ModelSerializer):
    """Сериализатор для типов ковров"""
    image = ImageFieldSerializer(required=False, allow_null=True)

    class Meta:
        model = TypeCarpetCollection
        fields = ["id", "type", "slug", "description", "image"]
        read_only_fields = ["id", "slug"]


class StyleSerializer(serializers.ModelSerializer):
    """Сериализатор для стилей"""

    class Meta:
        model = Style
        fields = ["id", "name", "slug"]
        read_only_fields = ["id", "slug"]


class RoomSerializer(serializers.ModelSerializer):
    """Сериализатор для комнат"""

    class Meta:
        model = Room
        fields = ["id", "name", "slug"]
        read_only_fields = ["id", "slug"]


class ColorSerializer(serializers.ModelSerializer):
    """Сериализатор для цветов"""

    class Meta:
        model = Color
        fields = ["id", "name", "slug", "hex_code"]
        read_only_fields = ["id", "slug"]


class CollectionListSerializer(serializers.ModelSerializer):
    """Сериализатор для списка коллекций"""
    type_name = serializers.CharField(source="type.type", read_only=True)
    carpets_count = serializers.IntegerField(source="carpets.count", read_only=True)
    image = ImageFieldSerializer(required=False, allow_null=True)

    class Meta:
        model = Collection
        fields = [
            "id",
            "name",
            "slug",
            "description",
            "image",
            "type_name",
            "is_new",
            "carpets_count",
            "created_at",
        ]
        read_only_fields = ["id", "slug", "created_at"]


class CollectionDetailSerializer(serializers.ModelSerializer):
    """Сериализатор для детальной информации о коллекции"""
    type = TypeCarpetCollectionSerializer(read_only=True)
    image = ImageFieldSerializer(required=False, allow_null=True)

    class Meta:
        model = Collection
        fields = [
            "id",
            "name",
            "slug",
            "description",
            "image",
            "type",
            "is_published",
            "is_new",
            "created_at",
            "update_at",
        ]
        read_only_fields = ["id", "slug", "created_at", "update_at"]


class CarpetListSerializer(serializers.ModelSerializer):
    """Сериализатор для списка ковров"""
    collection_name = serializers.CharField(source="collection.name", read_only=True)
    collection_slug = serializers.CharField(source="collection.slug", read_only=True)
    styles = StyleSerializer(many=True, read_only=True)
    rooms = RoomSerializer(many=True, read_only=True)
    colors = ColorSerializer(many=True, read_only=True)
    photo = ImageFieldSerializer(required=False, allow_null=True)

    class Meta:
        model = Carpet
        fields = [
            "id",
            "code",
            "photo",
            "collection_name",
            "collection_slug",
            "material",
            "is_new",
            "is_popular",
            "styles",
            "rooms",
            "colors",
            "watched",
            "created_at",
        ]
        read_only_fields = ["id", "watched", "created_at"]


class CarpetDetailSerializer(serializers.ModelSerializer):
    """Сериализатор для детальной информации о ковре"""
    collection = CollectionListSerializer(read_only=True)
    styles = StyleSerializer(many=True, read_only=True)
    rooms = RoomSerializer(many=True, read_only=True)
    colors = ColorSerializer(many=True, read_only=True)
    photo = ImageFieldSerializer(required=False, allow_null=True)

    class Meta:
        model = Carpet
        fields = [
            "id",
            "code",
            "photo",
            "collection",
            "material",
            "density",
            "base",
            "pile_height",
            "yarn_composition",
            "weight",
            "is_new",
            "is_popular",
            "roll",
            "styles",
            "rooms",
            "colors",
            "watched",
            "is_published",
            "created_at",
            "update_at",
        ]
        read_only_fields = ["id", "watched", "created_at", "update_at"]


class NewsListSerializer(serializers.ModelSerializer):
    """Сериализатор для списка новостей"""
    image = ImageFieldSerializer(required=False, allow_null=True)

    class Meta:
        model = News
        fields = [
            "id",
            "title",
            "slug",
            "description",
            "image",
            "created_at",
        ]
        read_only_fields = ["id", "slug", "created_at"]


class NewsDetailSerializer(serializers.ModelSerializer):
    """Сериализатор для детальной информации о новости"""
    image = ImageFieldSerializer(required=False, allow_null=True)

    class Meta:
        model = News
        fields = [
            "id",
            "title",
            "slug",
            "description",
            "content",
            "image",
            "is_published",
            "created_at",
            "update_at",
        ]
        read_only_fields = ["id", "slug", "created_at", "update_at"]


class GallerySerializer(serializers.ModelSerializer):
    """Сериализатор для галереи"""
    image = ImageFieldSerializer(required=False, allow_null=True)

    class Meta:
        model = Gallery
        fields = [
            "id",
            "title",
            "image",
            "description",
            "created_at",
            "order",
        ]
        read_only_fields = ["id", "created_at"]
