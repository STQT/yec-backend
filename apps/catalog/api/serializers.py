from rest_framework import serializers

from apps.catalog.models import (
    AboutImage,
    AboutPage,
    AdvantageCard,
    Carpet,
    CarpetCharacteristic,
    CarpetImage,
    Characteristic,
    Collection,
    Color,
    CompanyHistory,
    ContactFormSubmission,
    ContactPage,
    DealerRequest,
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
from .utils import get_language_from_request


class ImageFieldSerializer(serializers.ImageField):
    """Кастомное поле для изображений с полным URL"""
    def to_representation(self, value):
        if not value:
            return None
        request = self.context.get("request")
        if request:
            return request.build_absolute_uri(value.url)
        return value.url


class StyleSerializer(serializers.ModelSerializer):
    """Сериализатор для стилей"""

    class Meta:
        model = Style
        fields = ["id", "name", "slug"]
        read_only_fields = ["id", "slug"]
    
    def to_representation(self, instance):
        """Возвращает данные на языке из query параметра lang"""
        representation = super().to_representation(instance)
        request = self.context.get("request")
        
        if request:
            language = get_language_from_request(request)
            
            # Всегда используем языковые поля, если они доступны
            lang_suffix = f"_{language}" if language else ""
            lang_field = f"name{lang_suffix}"
            
            if hasattr(instance, lang_field):
                lang_value = getattr(instance, lang_field, None)
                if lang_value:
                    representation["name"] = lang_value
                elif not representation.get("name"):
                    representation["name"] = instance.name
            else:
                representation["name"] = instance.name
        
        return representation


class RoomSerializer(serializers.ModelSerializer):
    """Сериализатор для комнат"""

    class Meta:
        model = Room
        fields = ["id", "name", "slug"]
        read_only_fields = ["id", "slug"]
    
    def to_representation(self, instance):
        """Возвращает данные на языке из query параметра lang"""
        representation = super().to_representation(instance)
        request = self.context.get("request")
        
        if request:
            language = get_language_from_request(request)
            
            # Всегда используем языковые поля, если они доступны
            lang_suffix = f"_{language}" if language else ""
            lang_field = f"name{lang_suffix}"
            
            if hasattr(instance, lang_field):
                lang_value = getattr(instance, lang_field, None)
                if lang_value:
                    representation["name"] = lang_value
                elif not representation.get("name"):
                    representation["name"] = instance.name
            else:
                representation["name"] = instance.name
        
        return representation


class ColorSerializer(serializers.ModelSerializer):
    """Сериализатор для цветов"""

    class Meta:
        model = Color
        fields = ["id", "name", "slug", "hex_code"]
        read_only_fields = ["id", "slug"]
    
    def to_representation(self, instance):
        """Возвращает данные на языке из query параметра lang"""
        representation = super().to_representation(instance)
        request = self.context.get("request")
        
        if request:
            language = get_language_from_request(request)
            
            # Всегда используем языковые поля, если они доступны
            lang_suffix = f"_{language}" if language else ""
            lang_field = f"name{lang_suffix}"
            
            if hasattr(instance, lang_field):
                lang_value = getattr(instance, lang_field, None)
                if lang_value:
                    representation["name"] = lang_value
                elif not representation.get("name"):
                    representation["name"] = instance.name
            else:
                representation["name"] = instance.name
        
        return representation


class CollectionListSerializer(serializers.ModelSerializer):
    """Сериализатор для списка коллекций"""
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
            "is_new",
            "carpets_count",
            "created_at",
        ]
        read_only_fields = ["id", "slug", "created_at"]
    
    def to_representation(self, instance):
        """Возвращает данные на языке из query параметра lang"""
        representation = super().to_representation(instance)
        request = self.context.get("request")
        
        if request:
            language = get_language_from_request(request)
            
            # Всегда используем языковые поля, если они доступны
            lang_suffix = f"_{language}" if language else ""
            
            for field in ['name', 'description']:
                lang_field = f"{field}{lang_suffix}"
                if hasattr(instance, lang_field):
                    lang_value = getattr(instance, lang_field, None)
                    if lang_value:
                        representation[field] = lang_value
                    elif not representation.get(field):
                        representation[field] = getattr(instance, field, None)
                else:
                    representation[field] = getattr(instance, field, None)
        
        return representation


class CollectionDetailSerializer(serializers.ModelSerializer):
    """Сериализатор для детальной информации о коллекции"""
    image = ImageFieldSerializer(required=False, allow_null=True)

    class Meta:
        model = Collection
        fields = [
            "id",
            "name",
            "slug",
            "description",
            "image",
            "is_published",
            "is_new",
            "created_at",
            "update_at",
            # SEO поля
            "seo_title",
            "seo_description",
        ]
        read_only_fields = ["id", "slug", "created_at", "update_at"]
    
    def to_representation(self, instance):
        """Возвращает данные на языке из query параметра lang"""
        representation = super().to_representation(instance)
        request = self.context.get("request")
        
        if request:
            language = get_language_from_request(request)
            
            # Всегда используем языковые поля, если они доступны
            lang_suffix = f"_{language}" if language else ""
            
            for field in ['name', 'description']:
                lang_field = f"{field}{lang_suffix}"
                if hasattr(instance, lang_field):
                    lang_value = getattr(instance, lang_field, None)
                    if lang_value:
                        representation[field] = lang_value
                    elif not representation.get(field):
                        representation[field] = getattr(instance, field, None)
                else:
                    representation[field] = getattr(instance, field, None)
            
            # SEO поля
            for field in ['seo_title', 'seo_description']:
                lang_field = f"{field}{lang_suffix}"
                if hasattr(instance, lang_field):
                    lang_value = getattr(instance, lang_field, None)
                    if lang_value:
                        representation[field] = lang_value
                    elif not representation.get(field):
                        representation[field] = getattr(instance, field, None)
                else:
                    representation[field] = getattr(instance, field, None)
        
        return representation


class CharacteristicSerializer(serializers.ModelSerializer):
    """Сериализатор для характеристик"""
    
    class Meta:
        model = Characteristic
        fields = ["id", "name", "order"]
        read_only_fields = ["id"]
    
    def to_representation(self, instance):
        """Возвращает данные на языке из query параметра lang"""
        representation = super().to_representation(instance)
        request = self.context.get("request")
        
        if request:
            language = get_language_from_request(request)
            
            # Всегда используем языковые поля, если они доступны
            lang_suffix = f"_{language}" if language else ""
            lang_field = f"name{lang_suffix}"
            
            if hasattr(instance, lang_field):
                lang_value = getattr(instance, lang_field, None)
                if lang_value:
                    representation["name"] = lang_value
                elif not representation.get("name"):
                    representation["name"] = instance.name
            else:
                representation["name"] = instance.name
        
        return representation


class CarpetCharacteristicSerializer(serializers.ModelSerializer):
    """Сериализатор для характеристик ковра"""
    characteristic = CharacteristicSerializer(read_only=True)
    characteristic_id = serializers.PrimaryKeyRelatedField(
        queryset=Characteristic.objects.filter(is_active=True),
        source='characteristic',
        write_only=True,
        required=False
    )
    
    class Meta:
        model = CarpetCharacteristic
        fields = ["id", "characteristic", "characteristic_id", "value", "order"]
        read_only_fields = ["id"]
    
    def to_representation(self, instance):
        """Возвращает данные на языке из query параметра lang"""
        representation = super().to_representation(instance)
        request = self.context.get("request")
        
        if request:
            language = get_language_from_request(request)
            
            # Всегда используем языковые поля для value, если они доступны
            lang_suffix = f"_{language}" if language else ""
            lang_field = f"value{lang_suffix}"
            
            if hasattr(instance, lang_field):
                lang_value = getattr(instance, lang_field, None)
                if lang_value:
                    representation["value"] = lang_value
                elif not representation.get("value"):
                    representation["value"] = instance.value
            else:
                representation["value"] = instance.value
        
        return representation


class CarpetImageSerializer(serializers.ModelSerializer):
    """Сериализатор для изображений галереи ковра"""
    image = ImageFieldSerializer(required=False, allow_null=True)
    
    class Meta:
        model = CarpetImage
        fields = ["id", "image", "order"]
        read_only_fields = ["id"]


class CarpetListSerializer(serializers.ModelSerializer):
    """Сериализатор для списка ковров"""
    collection_name = serializers.SerializerMethodField()
    collection_slug = serializers.CharField(source="collection.slug", read_only=True)
    styles = StyleSerializer(many=True, read_only=True)
    rooms = RoomSerializer(many=True, read_only=True)
    colors = ColorSerializer(many=True, read_only=True)
    photo = ImageFieldSerializer(required=False, allow_null=True)
    gallery_images = serializers.SerializerMethodField()
    characteristics = serializers.SerializerMethodField()

    class Meta:
        model = Carpet
        fields = [
            "id",
            "code",
            "photo",
            "collection_name",
            "collection_slug",
            "roll",
            "is_new",
            "is_popular",
            "styles",
            "rooms",
            "colors",
            "characteristics",
            "gallery_images",
            "watched",
            "created_at",
        ]
        read_only_fields = ["id", "watched", "created_at"]
    
    def get_gallery_images(self, obj):
        """Получить список изображений галереи ковра"""
        images = obj.gallery_images.all().order_by('order')
        return CarpetImageSerializer(images, many=True, context=self.context).data
    
    def get_characteristics(self, obj):
        """Получить список характеристик ковра"""
        characteristics = obj.characteristics.all().order_by('order', 'characteristic__order')
        return CarpetCharacteristicSerializer(characteristics, many=True, context=self.context).data
    
    def get_collection_name(self, obj):
        """Получить название коллекции на нужном языке"""
        request = self.context.get("request")
        if request:
            language = get_language_from_request(request)
            lang_suffix = f"_{language}" if language else ""
            lang_field = f"name{lang_suffix}"
            
            collection = obj.collection
            if hasattr(collection, lang_field):
                lang_value = getattr(collection, lang_field, None)
                if lang_value:
                    return lang_value
            return collection.name
        return obj.collection.name
    
    def to_representation(self, instance):
        """Возвращает данные на языке из query параметра lang"""
        representation = super().to_representation(instance)
        request = self.context.get("request")
        
        if request:
            language = get_language_from_request(request)
            
            # Всегда используем языковые поля для code, если они доступны
            lang_suffix = f"_{language}" if language else ""
            lang_field = f"code{lang_suffix}"
            
            if hasattr(instance, lang_field):
                lang_value = getattr(instance, lang_field, None)
                if lang_value:
                    representation["code"] = lang_value
                elif not representation.get("code"):
                    representation["code"] = instance.code
            else:
                representation["code"] = instance.code
        
        return representation


class CarpetDetailSerializer(serializers.ModelSerializer):
    """Сериализатор для детальной информации о ковре"""
    collection = CollectionListSerializer(read_only=True)
    styles = StyleSerializer(many=True, read_only=True)
    rooms = RoomSerializer(many=True, read_only=True)
    colors = ColorSerializer(many=True, read_only=True)
    photo = ImageFieldSerializer(required=False, allow_null=True)
    gallery_images = serializers.SerializerMethodField()
    characteristics = serializers.SerializerMethodField()

    class Meta:
        model = Carpet
        fields = [
            "id",
            "code",
            "photo",
            "collection",
            "is_new",
            "is_popular",
            "roll",
            "styles",
            "rooms",
            "colors",
            "characteristics",
            "gallery_images",
            "watched",
            "is_published",
            "created_at",
            "update_at",
        ]
        read_only_fields = ["id", "watched", "created_at", "update_at"]
    
    def get_gallery_images(self, obj):
        """Получить список изображений галереи ковра"""
        images = obj.gallery_images.all().order_by('order')
        return CarpetImageSerializer(images, many=True, context=self.context).data
    
    def get_characteristics(self, obj):
        """Получить список характеристик ковра"""
        characteristics = obj.characteristics.all().order_by('order', 'characteristic__order')
        return CarpetCharacteristicSerializer(characteristics, many=True, context=self.context).data
    
    def to_representation(self, instance):
        """Возвращает данные на языке из query параметра lang"""
        representation = super().to_representation(instance)
        request = self.context.get("request")
        
        if request:
            language = get_language_from_request(request)
            
            # Всегда используем языковые поля для code, если они доступны
            lang_suffix = f"_{language}" if language else ""
            lang_field = f"code{lang_suffix}"
            
            if hasattr(instance, lang_field):
                lang_value = getattr(instance, lang_field, None)
                if lang_value:
                    representation["code"] = lang_value
                elif not representation.get("code"):
                    representation["code"] = instance.code
            else:
                representation["code"] = instance.code
        
        return representation




class NewsImageSerializer(serializers.ModelSerializer):
    """Сериализатор для изображений новости"""
    image = ImageFieldSerializer(required=False, allow_null=True)
    
    class Meta:
        model = NewsImage
        fields = ["id", "image", "order"]
        read_only_fields = ["id"]


class NewsListSerializer(serializers.ModelSerializer):
    """Сериализатор для списка новостей"""
    cover_image = ImageFieldSerializer(required=False, allow_null=True)

    class Meta:
        model = News
        fields = [
            "id",
            "title",
            "slug",
            "cover_image",
            "created_at",
        ]
        read_only_fields = ["id", "slug", "created_at"]
    
    def to_representation(self, instance):
        """Возвращает данные на языке из query параметра lang"""
        representation = super().to_representation(instance)
        request = self.context.get("request")
        
        if request:
            language = get_language_from_request(request)
            lang_suffix = f"_{language}" if language else ""
            lang_field = f"title{lang_suffix}"
            
            if hasattr(instance, lang_field):
                lang_value = getattr(instance, lang_field, None)
                if lang_value:
                    representation["title"] = lang_value
                elif not representation.get("title"):
                    representation["title"] = instance.title
            else:
                representation["title"] = instance.title
        
        return representation


class NewsDetailSerializer(serializers.ModelSerializer):
    """Сериализатор для детальной информации о новости"""
    cover_image = ImageFieldSerializer(required=False, allow_null=True)
    images = serializers.SerializerMethodField()

    class Meta:
        model = News
        fields = [
            "id",
            "title",
            "slug",
            "cover_image",
            "paragraph_1",
            "paragraph_2",
            "images",
            "is_published",
            "created_at",
            "update_at",
            # SEO поля
            "seo_title",
            "seo_description",
        ]
        read_only_fields = ["id", "slug", "created_at", "update_at"]
    
    def get_images(self, obj):
        """Получить список изображений новости"""
        images = obj.images.all().order_by('order')
        return NewsImageSerializer(images, many=True, context=self.context).data
    
    def to_representation(self, instance):
        """Возвращает данные на языке из query параметра lang"""
        representation = super().to_representation(instance)
        request = self.context.get("request")
        
        if request:
            language = get_language_from_request(request)
            lang_suffix = f"_{language}" if language else ""
            
            # Title
            lang_field = f"title{lang_suffix}"
            if hasattr(instance, lang_field):
                lang_value = getattr(instance, lang_field, None)
                if lang_value:
                    representation["title"] = lang_value
                elif not representation.get("title"):
                    representation["title"] = instance.title
            else:
                representation["title"] = instance.title
            
            # Paragraphs
            for field in ['paragraph_1', 'paragraph_2']:
                lang_field = f"{field}{lang_suffix}"
                if hasattr(instance, lang_field):
                    lang_value = getattr(instance, lang_field, None)
                    if lang_value:
                        representation[field] = lang_value
                    elif not representation.get(field):
                        representation[field] = getattr(instance, field, None)
                else:
                    representation[field] = getattr(instance, field, None)
            
            # SEO поля
            for field in ['seo_title', 'seo_description']:
                lang_field = f"{field}{lang_suffix}"
                if hasattr(instance, lang_field):
                    lang_value = getattr(instance, lang_field, None)
                    if lang_value:
                        representation[field] = lang_value
                    elif not representation.get(field):
                        representation[field] = getattr(instance, field, None)
                else:
                    representation[field] = getattr(instance, field, None)
        
        return representation


class GallerySerializer(serializers.ModelSerializer):
    """Сериализатор для галереи"""
    image = ImageFieldSerializer(required=False, allow_null=True)

    class Meta:
        model = Gallery
        fields = [
            "id",
            "title",
            "image",
            "created_at",
            "order",
        ]
        read_only_fields = ["id", "created_at"]
    
    def to_representation(self, instance):
        """Возвращает данные на языке из query параметра lang"""
        representation = super().to_representation(instance)
        request = self.context.get("request")
        
        if request:
            language = get_language_from_request(request)
            lang_suffix = f"_{language}" if language else ""
            
            # Поле title
            lang_field = f"title{lang_suffix}"
            if hasattr(instance, lang_field):
                lang_value = getattr(instance, lang_field, None)
                if lang_value:
                    representation["title"] = lang_value
                elif not representation.get("title"):
                    representation["title"] = instance.title
            else:
                representation["title"] = instance.title
        
        return representation


class MainGallerySerializer(serializers.ModelSerializer):
    """Сериализатор для нижней галереи (одна запись)"""
    image_1 = ImageFieldSerializer(required=False, allow_null=True)
    image_2 = ImageFieldSerializer(required=False, allow_null=True)
    image_3 = ImageFieldSerializer(required=False, allow_null=True)
    image_4 = ImageFieldSerializer(required=False, allow_null=True)
    image_5 = ImageFieldSerializer(required=False, allow_null=True)
    image_6 = ImageFieldSerializer(required=False, allow_null=True)
    image_7 = ImageFieldSerializer(required=False, allow_null=True)
    image_8 = ImageFieldSerializer(required=False, allow_null=True)
    image_9 = ImageFieldSerializer(required=False, allow_null=True)
    image_10 = ImageFieldSerializer(required=False, allow_null=True)
    image_11 = ImageFieldSerializer(required=False, allow_null=True)
    image_12 = ImageFieldSerializer(required=False, allow_null=True)

    class Meta:
        model = MainGallery
        fields = [
            "id",
            "title",
            "image_1",
            "image_2",
            "image_3",
            "image_4",
            "image_5",
            "image_6",
            "image_7",
            "image_8",
            "image_9",
            "image_10",
            "image_11",
            "image_12",
            "created_at",
        ]
        read_only_fields = ["id", "created_at"]

    def to_representation(self, instance):
        """Возвращает данные на языке из query параметра lang"""
        representation = super().to_representation(instance)
        request = self.context.get("request")

        if request:
            language = get_language_from_request(request)
            lang_suffix = f"_{language}" if language else ""
            lang_field = f"title{lang_suffix}"
            if hasattr(instance, lang_field):
                lang_value = getattr(instance, lang_field, None)
                if lang_value:
                    representation["title"] = lang_value
                elif not representation.get("title"):
                    representation["title"] = instance.title
            else:
                representation["title"] = instance.title

        return representation


class AboutImageSerializer(serializers.ModelSerializer):
    """Сериализатор для изображений секции 'О нас'"""
    image = ImageFieldSerializer(required=False, allow_null=True)
    
    class Meta:
        model = AboutImage
        fields = ["id", "image", "order"]
        read_only_fields = ["id"]


class HomePageSerializer(serializers.ModelSerializer):
    """Сериализатор для главной страницы с поддержкой мультиязычности"""
    # Секция 1: Баннер
    banner_image = ImageFieldSerializer(required=False, allow_null=True)
    banner_video = serializers.FileField(required=False, allow_null=True)
    banner_showroom_image = ImageFieldSerializer(required=False, allow_null=True)
    
    # Секция 2: О нас
    about_images = serializers.SerializerMethodField()
    
    # Секция 3: Шоурум
    showroom_image = ImageFieldSerializer(required=False, allow_null=True)
    
    # Секция 4: Преимущества
    advantage_1_icon = serializers.FileField(required=False, allow_null=True)
    advantage_4_icon = serializers.FileField(required=False, allow_null=True)
    
    # Секция 5: Призыв к действию
    cta_image = ImageFieldSerializer(required=False, allow_null=True)
    
    # SEO поля
    og_image = ImageFieldSerializer(required=False, allow_null=True)
    
    class Meta:
        model = HomePage
        fields = [
            "id",
            # Секция 1: Баннер
            "banner_title",
            "banner_description",
            "banner_link",
            "banner_image",
            "banner_video",
            "banner_showroom_title",
            "banner_showroom_image",
            # Секция 2: О нас
            "about_section_title",
            "about_title",
            "about_link",
            "about_youtube_link",
            "about_bottom_description",
            "about_images",
            # Секция 3: Шоурум
            "showroom_image",
            "showroom_title",
            # Секция 4: Преимущества
            "advantage_title",
            "advantage_subtitle",
            "advantage_1_title",
            "advantage_1_icon",
            "advantage_1_description",
            "advantage_2_title",
            "advantage_2_description",
            "advantage_3_title",
            "advantage_3_description",
            "advantage_4_title",
            "advantage_4_icon",
            "advantage_4_description",
            # Секция 5: Призыв к действию
            "cta_title",
            "cta_description",
            "cta_image",
            # SEO поля
            "meta_title",
            "meta_description",
            "meta_keywords",
            "og_title",
            "og_description",
            "og_image",
            "canonical_url",
        ]
        read_only_fields = ["id"]
    
    def get_about_images(self, obj):
        """Получить список изображений секции 'О нас'"""
        images = obj.about_images.all().order_by('order')
        return AboutImageSerializer(images, many=True, context=self.context).data

    def to_representation(self, instance):
        """Возвращает данные на языке из query параметра lang"""
        representation = super().to_representation(instance)
        request = self.context.get("request")
        
        if request:
            # Получаем язык из query параметра
            language = get_language_from_request(request)
            lang_suffix = f"_{language}" if language else ""
            
            # Секция 1: Баннер
            multilingual_fields_banner = [
                'banner_title', 'banner_description', 'banner_link',
                'banner_showroom_title'
            ]
            for field in multilingual_fields_banner:
                lang_field = f"{field}{lang_suffix}"
                if hasattr(instance, lang_field):
                    value = getattr(instance, lang_field)
                    if value:
                        representation[field] = value
            
            # Секция 2: О нас
            multilingual_fields_about = [
                'about_section_title', 'about_title', 'about_link', 'about_youtube_link', 'about_bottom_description'
            ]
            for field in multilingual_fields_about:
                lang_field = f"{field}{lang_suffix}"
                if hasattr(instance, lang_field):
                    value = getattr(instance, lang_field)
                    if value:
                        representation[field] = value
            
            # Секция 3: Шоурум
            multilingual_fields_showroom = ['showroom_title']
            for field in multilingual_fields_showroom:
                lang_field = f"{field}{lang_suffix}"
                if hasattr(instance, lang_field):
                    value = getattr(instance, lang_field)
                    if value:
                        representation[field] = value
            
            # Секция 4: Преимущества
            # Общие поля секции
            multilingual_fields_advantage_section = ['advantage_title', 'advantage_subtitle']
            for field in multilingual_fields_advantage_section:
                lang_field = f"{field}{lang_suffix}"
                if hasattr(instance, lang_field):
                    value = getattr(instance, lang_field)
                    if value:
                        representation[field] = value
            
            # Поля карточек
            for i in range(1, 5):
                for subfield in ['title', 'description']:
                    field = f"advantage_{i}_{subfield}"
                    lang_field = f"{field}{lang_suffix}"
                    if hasattr(instance, lang_field):
                        value = getattr(instance, lang_field)
                    if value:
                        representation[field] = value
            
            # Секция 5: Призыв к действию
            multilingual_fields_cta = ['cta_title', 'cta_description']
            for field in multilingual_fields_cta:
                lang_field = f"{field}{lang_suffix}"
                if hasattr(instance, lang_field):
                    value = getattr(instance, lang_field)
                    if value:
                        representation[field] = value
            
            # SEO поля
            multilingual_fields_seo = [
                'meta_title', 'meta_description', 'meta_keywords',
                'og_title', 'og_description', 'canonical_url'
            ]
            for field in multilingual_fields_seo:
                lang_field = f"{field}{lang_suffix}"
                if hasattr(instance, lang_field):
                    value = getattr(instance, lang_field)
                    if value:
                        representation[field] = value
        
        return representation


class ProductionStepSerializer(serializers.ModelSerializer):
    """Сериализатор для этапов производства"""
    image = ImageFieldSerializer(required=False, allow_null=True)

    class Meta:
        model = ProductionStep
        fields = ["id", "title", "description", "image", "order"]
        read_only_fields = ["id"]
    
    def to_representation(self, instance):
        """Возвращает данные на языке из query параметра lang"""
        representation = super().to_representation(instance)
        request = self.context.get("request")
        
        if request:
            language = get_language_from_request(request)
            lang_suffix = f"_{language}" if language else ""
            
            for field in ['title', 'description']:
                lang_field = f"{field}{lang_suffix}"
                if hasattr(instance, lang_field):
                    value = getattr(instance, lang_field)
                    if value:
                        representation[field] = value
        
        return representation


class CompanyHistorySerializer(serializers.ModelSerializer):
    """Сериализатор для истории компании"""
    image = ImageFieldSerializer(required=False, allow_null=True)
    class Meta:
        model = CompanyHistory
        fields = ["id", "year", "year_title", "year_description", "image"]
        read_only_fields = ["id"]
    
    def to_representation(self, instance):
        """Возвращает данные на языке из query параметра lang"""
        representation = super().to_representation(instance)
        request = self.context.get("request")
        
        if request:
            language = get_language_from_request(request)
            lang_suffix = f"_{language}" if language else ""
            
            for field in ['year_title', 'year_description']:
                lang_field = f"{field}{lang_suffix}"
                if hasattr(instance, lang_field):
                    value = getattr(instance, lang_field)
                    if value:
                        representation[field] = value
        
        return representation


class AboutPageSerializer(serializers.ModelSerializer):
    """Сериализатор для страницы о компании с поддержкой мультиязычности"""
    # Секция 1: О компании
    about_image_1 = ImageFieldSerializer(required=False, allow_null=True)
    about_image_2 = ImageFieldSerializer(required=False, allow_null=True)
    
    # Секция 4: Объемы производства
    capacity_card_1_image = ImageFieldSerializer(required=False, allow_null=True)
    capacity_card_2_image = ImageFieldSerializer(required=False, allow_null=True)
    capacity_card_3_image = ImageFieldSerializer(required=False, allow_null=True)
    capacity_card_4_image = ImageFieldSerializer(required=False, allow_null=True)
    
    # Динамические секции
    production_steps = serializers.SerializerMethodField()
    company_history = serializers.SerializerMethodField()
    
    # SEO поля
    og_image = ImageFieldSerializer(required=False, allow_null=True)

    class Meta:
        model = AboutPage
        fields = [
            "id",
            # Секция 1: О компании
            "about_section_title",
            "about_banner_title",
            "about_banner_subtitle",
            "about_image_1",
            "about_image_2",
            # Секция 2: Процесс производства
            "production_section_title",
            "production_title",
            "production_steps",
            # Секция 3: История компании
            "history_section_title",
            "company_history",
            # Секция 4: Объемы производства
            "capacity_section_title",
            "capacity_title",
            "capacity_card_1_title",
            "capacity_card_1_subtitle",
            "capacity_card_1_image",
            "capacity_card_2_title",
            "capacity_card_2_subtitle",
            "capacity_card_2_image",
            "capacity_card_3_title",
            "capacity_card_3_subtitle",
            "capacity_card_3_image",
            "capacity_card_4_title",
            "capacity_card_4_subtitle",
            "capacity_card_4_image",
            # Секция 5: Партнерство для дилеров
            "dealer_section_title",
            "dealer_title",
            "dealer_card_1_title",
            "dealer_card_1_description",
            "dealer_card_2_title",
            "dealer_card_2_description",
            "dealer_card_3_title",
            "dealer_card_3_description",
            # SEO поля
            "meta_title",
            "meta_description",
            "meta_keywords",
            "og_title",
            "og_description",
            "og_image",
            "canonical_url",
        ]
        read_only_fields = ["id"]
    
    def get_production_steps(self, obj):
        """Получить этапы производства с учетом языка"""
        steps = obj.production_steps.all().order_by('order')
        request = self.context.get("request")
        
        if request:
            language = get_language_from_request(request)
            
            data = []
            for step in steps:
                item = {
                    "id": step.id,
                    "order": step.order,
                    "title": getattr(step, f"title_{language}", step.title) if language != "uz" else step.title,
                    "description": getattr(step, f"description_{language}", step.description) if language != "uz" else step.description,
                    "image": request.build_absolute_uri(step.image.url) if step.image else None,
                }
                data.append(item)
            return data
        
        return ProductionStepSerializer(steps, many=True, context=self.context).data
    
    def get_company_history(self, obj):
        """Получить историю компании с учетом языка"""
        history = obj.company_history.all().order_by('year')
        return CompanyHistorySerializer(history, many=True, context=self.context).data

    def to_representation(self, instance):
        """Возвращает данные на языке из query параметра lang"""
        representation = super().to_representation(instance)
        request = self.context.get("request")
        
        if request:
            language = get_language_from_request(request)
            lang_suffix = f"_{language}" if language else ""
            
            # Секция 1: О компании
            multilingual_fields_about = [
                'about_section_title', 'about_banner_title', 'about_banner_subtitle'
            ]
            for field in multilingual_fields_about:
                lang_field = f"{field}{lang_suffix}"
                if hasattr(instance, lang_field):
                    value = getattr(instance, lang_field)
                    if value:
                        representation[field] = value
            
            # Секция 2: Процесс производства
            multilingual_fields_production = [
                'production_section_title', 'production_title'
            ]
            for field in multilingual_fields_production:
                lang_field = f"{field}{lang_suffix}"
                if hasattr(instance, lang_field):
                    value = getattr(instance, lang_field)
                    if value:
                        representation[field] = value
            
            # Секция 3: История компании
            multilingual_fields_history = ['history_section_title']
            for field in multilingual_fields_history:
                lang_field = f"{field}{lang_suffix}"
                if hasattr(instance, lang_field):
                    value = getattr(instance, lang_field)
                    if value:
                        representation[field] = value
            
            # Секция 4: Объемы производства
            multilingual_fields_capacity = [
                'capacity_section_title', 'capacity_title',
                'capacity_card_1_title', 'capacity_card_1_subtitle',
                'capacity_card_2_title', 'capacity_card_2_subtitle',
                'capacity_card_3_title', 'capacity_card_3_subtitle',
                'capacity_card_4_title', 'capacity_card_4_subtitle',
            ]
            for field in multilingual_fields_capacity:
                lang_field = f"{field}{lang_suffix}"
                if hasattr(instance, lang_field):
                    value = getattr(instance, lang_field)
                    if value:
                        representation[field] = value
            
            # Секция 5: Партнерство для дилеров
            multilingual_fields_dealer = [
                'dealer_section_title', 'dealer_title',
                'dealer_card_1_title', 'dealer_card_1_description',
                'dealer_card_2_title', 'dealer_card_2_description',
                'dealer_card_3_title', 'dealer_card_3_description',
            ]
            for field in multilingual_fields_dealer:
                lang_field = f"{field}{lang_suffix}"
                if hasattr(instance, lang_field):
                    value = getattr(instance, lang_field)
                    if value:
                        representation[field] = value
            
            # SEO поля
            multilingual_fields_seo = [
                'meta_title', 'meta_description', 'meta_keywords',
                'og_title', 'og_description', 'canonical_url'
            ]
            for field in multilingual_fields_seo:
                lang_field = f"{field}{lang_suffix}"
                if hasattr(instance, lang_field):
                    value = getattr(instance, lang_field)
                    if value:
                        representation[field] = value
        
        return representation


class ContactPageSerializer(serializers.ModelSerializer):
    """Сериализатор для страницы контактов"""
    # SEO поля
    og_image = ImageFieldSerializer(required=False, allow_null=True)
    
    class Meta:
        model = ContactPage
        fields = [
            "id",
            "page_title",
            "address_label",
            "address",
            "phone_label",
            "phone",
            "email_label",
            "email",
            "map_embed_url",
            "form_title",
            "form_description",
            "facebook_url",
            "twitter_url",
            "linkedin_url",
            "instagram_url",
            # SEO поля
            "meta_title",
            "meta_description",
            "meta_keywords",
            "og_title",
            "og_description",
            "og_image",
            "canonical_url",
        ]
        read_only_fields = ["id"]
    
    def to_representation(self, instance):
        """Возвращает данные на языке из query параметра lang"""
        representation = super().to_representation(instance)
        request = self.context.get("request")
        
        if request:
            language = get_language_from_request(request)
            
            if language and language != "uz":
                representation["page_title"] = getattr(instance, f"page_title_{language}", instance.page_title)
                representation["address_label"] = getattr(instance, f"address_label_{language}", instance.address_label)
                representation["address"] = getattr(instance, f"address_{language}", instance.address)
                representation["phone_label"] = getattr(instance, f"phone_label_{language}", instance.phone_label)
                representation["email_label"] = getattr(instance, f"email_label_{language}", instance.email_label)
                representation["form_title"] = getattr(instance, f"form_title_{language}", instance.form_title)
                representation["form_description"] = getattr(instance, f"form_description_{language}", instance.form_description)
            
            # SEO поля
            multilingual_fields_seo = [
                'meta_title', 'meta_description', 'meta_keywords',
                'og_title', 'og_description', 'canonical_url'
            ]
            lang_suffix = f"_{language}" if language else ""
            for field in multilingual_fields_seo:
                lang_field = f"{field}{lang_suffix}"
                if hasattr(instance, lang_field):
                    value = getattr(instance, lang_field)
                    if value:
                        representation[field] = value
        
        return representation


class SalesPointSerializer(serializers.ModelSerializer):
    """Сериализатор для торговой точки"""
    
    class Meta:
        model = SalesPoint
        fields = [
            "id",
            "name",
            "address",
            "location",
            "phone",
            "map_link",
            "order",
        ]
        read_only_fields = ["id"]
    
    def to_representation(self, instance):
        """Возвращает данные на языке из query параметра lang"""
        representation = super().to_representation(instance)
        request = self.context.get("request")
        
        if request:
            language = get_language_from_request(request)
            
            if language and language != "uz":
                representation["name"] = getattr(instance, f"name_{language}", instance.name)
                representation["address"] = getattr(instance, f"address_{language}", instance.address)
                representation["location"] = getattr(instance, f"location_{language}", instance.location)
        
        return representation


class RegionSerializer(serializers.ModelSerializer):
    """Сериализатор для региона со списком торговых точек"""
    sales_points = serializers.SerializerMethodField()
    
    class Meta:
        model = Region
        fields = [
            "id",
            "name",
            "slug",
            "sales_points",
        ]
        read_only_fields = ["id", "slug"]
    
    def get_sales_points(self, obj):
        """Получить торговые точки региона с учетом языка"""
        points = obj.sales_points.filter(is_published=True).order_by('order')
        request = self.context.get("request")
        
        if request:
            language = get_language_from_request(request)
            
            data = []
            for point in points:
                item = {
                    "id": point.id,
                    "name": getattr(point, f"name_{language}", point.name) if language != "uz" else point.name,
                    "address": getattr(point, f"address_{language}", point.address) if language != "uz" else point.address,
                    "location": getattr(point, f"location_{language}", point.location) if language != "uz" else point.location,
                    "phone": point.phone,
                    "map_link": point.map_link,
                    "order": point.order,
                }
                data.append(item)
            return data
        
        return SalesPointSerializer(points, many=True, context={"request": request}).data
    
    def to_representation(self, instance):
        """Возвращает данные на языке из query параметра lang"""
        representation = super().to_representation(instance)
        request = self.context.get("request")
        
        if request:
            language = get_language_from_request(request)
            
            # Всегда используем языковые поля, если они доступны
            lang_suffix = f"_{language}" if language else ""
            lang_field = f"name{lang_suffix}"
            
            if hasattr(instance, lang_field):
                lang_value = getattr(instance, lang_field, None)
                if lang_value:
                    representation["name"] = lang_value
                elif not representation.get("name"):
                    representation["name"] = instance.name
            else:
                representation["name"] = instance.name
        
        return representation


class ContactFormSubmissionSerializer(serializers.ModelSerializer):
    """Сериализатор для создания заявки"""
    
    class Meta:
        model = ContactFormSubmission
        fields = ["name", "phone", "email", "message"]
    
    def create(self, validated_data):
        """Создать новую заявку со статусом 'new'"""
        validated_data['status'] = 'new'
        return super().create(validated_data)


class DealerRequestSerializer(serializers.ModelSerializer):
    """Сериализатор для заявок на дилерство"""
    
    class Meta:
        model = DealerRequest
        fields = ["name", "company", "email", "message"]
    
    def validate_email(self, value):
        """Валидация email"""
        if not value:
            raise serializers.ValidationError("Email обязателен для заполнения")
        return value
    
    def validate_name(self, value):
        """Валидация имени"""
        if not value or len(value.strip()) < 2:
            raise serializers.ValidationError("Имя должно содержать минимум 2 символа")
        return value.strip()
    
    def validate_company(self, value):
        """Валидация названия компании"""
        if not value or len(value.strip()) < 2:
            raise serializers.ValidationError("Название компании должно содержать минимум 2 символа")
        return value.strip()
    
    def validate_message(self, value):
        """Валидация сообщения"""
        if not value or len(value.strip()) < 10:
            raise serializers.ValidationError("Текст обращения должен содержать минимум 10 символов")
        return value.strip()


class FAQSerializer(serializers.ModelSerializer):
    """Сериализатор для FAQ"""
    
    class Meta:
        model = FAQ
        fields = ["id", "question", "answer", "order"]
        read_only_fields = ["id"]
    
    def to_representation(self, instance):
        """Возвращает данные на языке из query параметра lang"""
        representation = super().to_representation(instance)
        request = self.context.get("request")
        
        if request:
            language = get_language_from_request(request)
            
            if language and language != "uz":
                representation["question"] = getattr(instance, f"question_{language}", instance.question)
                representation["answer"] = getattr(instance, f"answer_{language}", instance.answer)
        
        return representation


class AdvantageCardSerializer(serializers.ModelSerializer):
    """Сериализатор для карточек преимуществ"""
    
    class Meta:
        model = AdvantageCard
        fields = ["id", "title", "description", "svg_icon", "order"]
        read_only_fields = ["id"]
    
    def to_representation(self, instance):
        """Возвращает данные на языке из query параметра lang"""
        representation = super().to_representation(instance)
        request = self.context.get("request")
        
        if request:
            language = get_language_from_request(request)
            
            if language and language != "uz":
                representation["title"] = getattr(instance, f"title_{language}", instance.title)
                representation["description"] = getattr(instance, f"description_{language}", instance.description)
        
        return representation


class InstagramPostSerializer(serializers.ModelSerializer):
    """Сериализатор для постов Instagram"""
    post_type_display = serializers.CharField(source='get_post_type_display', read_only=True)
    
    class Meta:
        model = InstagramPost
        fields = [
            "id",
            "instagram_id",
            "post_type",
            "post_type_display",
            "caption",
            "permalink",
            "thumbnail_url",
            "media_url",
            "like_count",
            "comments_count",
            "timestamp",
            "is_published",
            "created_at",
        ]
        read_only_fields = ["id", "created_at", "updated_at"]


class GlobalSettingsSerializer(serializers.ModelSerializer):
    """Сериализатор для глобальных настроек"""
    collection_cover_image = ImageFieldSerializer(required=False, allow_null=True)
    product_cover_image = ImageFieldSerializer(required=False, allow_null=True)
    
    class Meta:
        model = GlobalSettings
        fields = [
            "id",
            "copyright",
            "form_modal_title",
            "form_modal_text",
            "success_modal_title",
            "success_modal_text",
            "dealer_form_title",
            "dealer_form_description",
            "email",
            "address",
            "phone",
            "tour_3d_link",
            "collection_cover_image",
            "product_cover_image",
            # SEO поля для страниц
            "collections_seo_title",
            "collections_seo_description",
            "news_seo_title",
            "news_seo_description",
            "gallery_seo_title",
            "gallery_seo_description",
            "is_published",
            "created_at",
            "update_at",
        ]
        read_only_fields = ["id", "created_at", "update_at"]
    
    def to_representation(self, instance):
        """Возвращает данные на языке из query параметра lang"""
        representation = super().to_representation(instance)
        request = self.context.get("request")
        
        if request:
            language = get_language_from_request(request)
            lang_suffix = f"_{language}" if language else ""
            
            # Мультиязычные поля
            multilingual_fields = [
                'copyright',
                'form_modal_title',
                'form_modal_text',
                'success_modal_title',
                'success_modal_text',
                'dealer_form_title',
                'dealer_form_description',
                'address',
                # SEO поля
                'collections_seo_title',
                'collections_seo_description',
                'news_seo_title',
                'news_seo_description',
                'gallery_seo_title',
                'gallery_seo_description',
            ]
            
            for field in multilingual_fields:
                lang_field = f"{field}{lang_suffix}"
                if hasattr(instance, lang_field):
                    value = getattr(instance, lang_field)
                    if value:
                        representation[field] = value
        
        return representation
