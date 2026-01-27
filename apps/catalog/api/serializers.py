from rest_framework import serializers

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


class PointTypeSerializer(serializers.ModelSerializer):
    """Сериализатор для типов точек"""

    class Meta:
        model = PointType
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
        
        return representation


class CarpetListSerializer(serializers.ModelSerializer):
    """Сериализатор для списка ковров"""
    collection_name = serializers.SerializerMethodField()
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
            "density",
            "base",
            "pile_height",
            "yarn_composition",
            "weight",
            "roll",
            "is_new",
            "is_popular",
            "styles",
            "rooms",
            "colors",
            "watched",
            "created_at",
        ]
        read_only_fields = ["id", "watched", "created_at"]
    
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
            
            # Всегда используем языковые поля, если они доступны
            # Для uz используем code_uz, material_uz и т.д., если они есть
            lang_suffix = f"_{language}" if language else ""
            
            # Получаем значение с учетом языка, если поле существует
            multilingual_fields = ['code', 'material', 'density', 'base', 'pile_height', 'yarn_composition', 'weight']
            
            for field in multilingual_fields:
                lang_field = f"{field}{lang_suffix}"
                # Проверяем, существует ли языковое поле и есть ли в нем значение
                if hasattr(instance, lang_field):
                    lang_value = getattr(instance, lang_field, None)
                    if lang_value:
                        representation[field] = lang_value
                    # Если языковое поле пустое, используем базовое поле как fallback
                    elif not representation.get(field):
                        representation[field] = getattr(instance, field, None)
                else:
                    # Если языкового поля нет, используем базовое поле
                    representation[field] = getattr(instance, field, None)
        
        return representation


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
    
    def to_representation(self, instance):
        """Возвращает данные на языке из query параметра lang"""
        representation = super().to_representation(instance)
        request = self.context.get("request")
        
        if request:
            language = get_language_from_request(request)
            
            # Всегда используем языковые поля, если они доступны
            lang_suffix = f"_{language}" if language else ""
            
            # Получаем значение с учетом языка, если поле существует
            multilingual_fields = ['code', 'material', 'density', 'base', 'pile_height', 'yarn_composition', 'weight']
            
            for field in multilingual_fields:
                lang_field = f"{field}{lang_suffix}"
                # Проверяем, существует ли языковое поле и есть ли в нем значение
                if hasattr(instance, lang_field):
                    lang_value = getattr(instance, lang_field, None)
                    if lang_value:
                        representation[field] = lang_value
                    # Если языковое поле пустое, используем базовое поле как fallback
                    elif not representation.get(field):
                        representation[field] = getattr(instance, field, None)
                else:
                    # Если языкового поля нет, используем базовое поле
                    representation[field] = getattr(instance, field, None)
        
        return representation


class NewsImageSerializer(serializers.ModelSerializer):
    """Сериализатор для изображений блока контента"""
    image = ImageFieldSerializer(required=False, allow_null=True)
    
    class Meta:
        model = NewsImage
        fields = ["id", "image", "caption", "order"]
        read_only_fields = ["id"]


class NewsContentBlockSerializer(serializers.ModelSerializer):
    """Сериализатор для блоков контента новости"""
    images = serializers.SerializerMethodField()
    
    class Meta:
        model = NewsContentBlock
        fields = ["id", "content_type", "title", "text_content", "images", "order"]
        read_only_fields = ["id"]
    
    def get_images(self, obj):
        """Получить изображения блока (только для блоков типа images)"""
        if obj.content_type == 'images':
            images = obj.images.all().order_by('order')[:3]  # Максимум 3 изображения
            request = self.context.get("request")
            
            if request:
                language = get_language_from_request(request)
                
                data = []
                for image in images:
                    item = {
                        "id": image.id,
                        "image": request.build_absolute_uri(image.image.url) if image.image else None,
                        "caption": getattr(image, f"caption_{language}", image.caption) if language != "uz" else image.caption,
                        "order": image.order,
                    }
                    data.append(item)
                return data
            
            return NewsImageSerializer(images, many=True, context=self.context).data
        return []
    
    def to_representation(self, instance):
        """Возвращает данные на языке из query параметра lang"""
        representation = super().to_representation(instance)
        request = self.context.get("request")
        
        if request:
            language = get_language_from_request(request)
            
            if language and language != "uz":
                representation["title"] = getattr(instance, f"title_{language}", instance.title)
                representation["text_content"] = getattr(instance, f"text_content_{language}", instance.text_content)
        
        return representation


class NewsListSerializer(serializers.ModelSerializer):
    """Сериализатор для списка новостей"""
    cover_image = ImageFieldSerializer(required=False, allow_null=True)

    class Meta:
        model = News
        fields = [
            "id",
            "title",
            "slug",
            "description",
            "cover_image",
            "created_at",
        ]
        read_only_fields = ["id", "slug", "created_at"]


class NewsDetailSerializer(serializers.ModelSerializer):
    """Сериализатор для детальной информации о новости с динамическими блоками контента"""
    cover_image = ImageFieldSerializer(required=False, allow_null=True)
    content_blocks = serializers.SerializerMethodField()

    class Meta:
        model = News
        fields = [
            "id",
            "title",
            "slug",
            "description",
            "cover_image",
            "content_blocks",
            "is_published",
            "created_at",
            "update_at",
        ]
        read_only_fields = ["id", "slug", "created_at", "update_at"]
    
    def get_content_blocks(self, obj):
        """Получить блоки контента с учетом языка"""
        blocks = obj.content_blocks.all().order_by('order')
        request = self.context.get("request")
        
        if request:
            language = get_language_from_request(request)
            
            data = []
            for block in blocks:
                item = {
                    "id": block.id,
                    "content_type": block.content_type,
                    "order": block.order,
                }
                
                # Добавляем текстовое содержание для текстовых блоков
                if block.content_type == 'text':
                    item["text_content"] = getattr(block, f"text_content_{language}", block.text_content) if language != "uz" else block.text_content
                
                # Добавляем изображения для блоков изображений
                if block.content_type == 'images':
                    images = block.images.all().order_by('order')[:3]
                    item["images"] = []
                    for image in images:
                        img_data = {
                            "id": image.id,
                            "image": request.build_absolute_uri(image.image.url) if image.image else None,
                            "caption": getattr(image, f"caption_{language}", image.caption) if language != "uz" else image.caption,
                            "order": image.order,
                        }
                        item["images"].append(img_data)
                
                data.append(item)
            return data
        
        return NewsContentBlockSerializer(blocks, many=True, context=self.context).data


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


class HomePageSerializer(serializers.ModelSerializer):
    """Сериализатор для главной страницы с поддержкой мультиязычности"""
    image = ImageFieldSerializer(required=False, allow_null=True)
    video = serializers.FileField(required=False, allow_null=True)
    
    class Meta:
        model = HomePage
        fields = [
            "id",
            "image",
            "video",
            "title",
            "description",
            "collection_link",
            "showroom_title",
            "showroom_link",
        ]
        read_only_fields = ["id"]

    def to_representation(self, instance):
        """Возвращает данные на языке из query параметра lang"""
        representation = super().to_representation(instance)
        request = self.context.get("request")
        
        if request:
            # Получаем язык из query параметра
            language = get_language_from_request(request)
            
            # Получаем переведенные поля
            if language and language != "uz":  # uz - язык по умолчанию
                representation["title"] = getattr(instance, f"title_{language}", instance.title)
                representation["description"] = getattr(instance, f"description_{language}", instance.description)
                representation["collection_link"] = getattr(instance, f"collection_link_{language}", instance.collection_link)
                representation["showroom_title"] = getattr(instance, f"showroom_title_{language}", instance.showroom_title)
                representation["showroom_link"] = getattr(instance, f"showroom_link_{language}", instance.showroom_link)
        
        return representation


class ProductionStepSerializer(serializers.ModelSerializer):
    """Сериализатор для этапов производства"""
    image = ImageFieldSerializer(required=False, allow_null=True)

    class Meta:
        model = ProductionStep
        fields = ["id", "title", "description", "image", "order"]
        read_only_fields = ["id"]


class CompanyHistorySerializer(serializers.ModelSerializer):
    """Сериализатор для истории компании"""
    image = ImageFieldSerializer(required=False, allow_null=True)

    class Meta:
        model = CompanyHistory
        fields = ["id", "year", "title", "description", "image", "order"]
        read_only_fields = ["id"]


class ProductionCapacitySerializer(serializers.ModelSerializer):
    """Сериализатор для объемов производства"""
    image = ImageFieldSerializer(required=False, allow_null=True)

    class Meta:
        model = ProductionCapacity
        fields = ["id", "year", "capacity", "description", "image", "order"]
        read_only_fields = ["id"]


class DealerAdvantageSerializer(serializers.ModelSerializer):
    """Сериализатор для преимуществ дилеров"""

    class Meta:
        model = DealerAdvantage
        fields = ["id", "title", "description", "order"]
        read_only_fields = ["id"]


class AboutPageSerializer(serializers.ModelSerializer):
    """Сериализатор для страницы о компании с поддержкой мультиязычности"""
    main_image = ImageFieldSerializer(required=False, allow_null=True)
    showroom_image = ImageFieldSerializer(required=False, allow_null=True)
    production_steps = serializers.SerializerMethodField()
    company_history = serializers.SerializerMethodField()
    production_capacity = serializers.SerializerMethodField()
    dealer_advantages = serializers.SerializerMethodField()

    class Meta:
        model = AboutPage
        fields = [
            "id",
            "company_title",
            "company_subtitle",
            "company_description",
            "main_image",
            "showroom_image",
            "production_section_title",
            "history_section_title",
            "capacity_section_title",
            "dealer_section_title",
            "showroom_button_text",
            "production_steps",
            "company_history",
            "production_capacity",
            "dealer_advantages",
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
        history = obj.company_history.all().order_by('order', 'year')
        request = self.context.get("request")
        
        if request:
            language = get_language_from_request(request)
            
            data = []
            for item in history:
                history_item = {
                    "id": item.id,
                    "year": item.year,
                    "order": item.order,
                    "title": getattr(item, f"title_{language}", item.title) if language != "uz" else item.title,
                    "description": getattr(item, f"description_{language}", item.description) if language != "uz" else item.description,
                    "image": request.build_absolute_uri(item.image.url) if item.image else None,
                }
                data.append(history_item)
            return data
        
        return CompanyHistorySerializer(history, many=True, context=self.context).data
    
    def get_production_capacity(self, obj):
        """Получить объемы производства с учетом языка"""
        capacity = obj.production_capacity.all().order_by('order', 'year')
        request = self.context.get("request")
        
        if request:
            language = get_language_from_request(request)
            
            data = []
            for item in capacity:
                capacity_item = {
                    "id": item.id,
                    "year": item.year,
                    "order": item.order,
                    "capacity": getattr(item, f"capacity_{language}", item.capacity) if language != "uz" else item.capacity,
                    "description": getattr(item, f"description_{language}", item.description) if language != "uz" else item.description,
                    "image": request.build_absolute_uri(item.image.url) if item.image else None,
                }
                data.append(capacity_item)
            return data
        
        return ProductionCapacitySerializer(capacity, many=True, context=self.context).data
    
    def get_dealer_advantages(self, obj):
        """Получить преимущества дилеров с учетом языка"""
        advantages = obj.dealer_advantages.filter(is_published=True).order_by('order')
        request = self.context.get("request")
        
        if request:
            language = get_language_from_request(request)
            
            data = []
            for advantage in advantages:
                item = {
                    "id": advantage.id,
                    "order": advantage.order,
                    "title": getattr(advantage, f"title_{language}", advantage.title) if language != "uz" else advantage.title,
                    "description": getattr(advantage, f"description_{language}", advantage.description) if language != "uz" else advantage.description,
                }
                data.append(item)
            return data
        
        return DealerAdvantageSerializer(advantages, many=True).data

    def to_representation(self, instance):
        """Возвращает данные на языке из query параметра lang"""
        representation = super().to_representation(instance)
        request = self.context.get("request")
        
        if request:
            # Получаем язык из query параметра
            language = get_language_from_request(request)
            
            # Получаем переведенные поля для основной информации
            if language and language != "uz":  # uz - язык по умолчанию
                representation["company_title"] = getattr(instance, f"company_title_{language}", instance.company_title)
                representation["company_subtitle"] = getattr(instance, f"company_subtitle_{language}", instance.company_subtitle)
                representation["company_description"] = getattr(instance, f"company_description_{language}", instance.company_description)
                representation["production_section_title"] = getattr(instance, f"production_section_title_{language}", instance.production_section_title)
                representation["history_section_title"] = getattr(instance, f"history_section_title_{language}", instance.history_section_title)
                representation["capacity_section_title"] = getattr(instance, f"capacity_section_title_{language}", instance.capacity_section_title)
                representation["dealer_section_title"] = getattr(instance, f"dealer_section_title_{language}", instance.dealer_section_title)
                representation["showroom_button_text"] = getattr(instance, f"showroom_button_text_{language}", instance.showroom_button_text)
            
            # Переводим JSON поля
            representation["production_steps"] = self._translate_json_list(
                instance.production_steps, language, ["title", "description"]
            )
            representation["company_history"] = self._translate_json_list(
                instance.company_history, language, ["title", "description"]
            )
            representation["production_capacity"] = self._translate_json_list(
                instance.production_capacity, language, ["capacity", "description"]
            )
            # dealer_advantages обрабатывается через get_dealer_advantages()
        
        return representation

    def _translate_json_list(self, json_data, language, translatable_fields):
        """Переводит поля в JSON списке на нужный язык"""
        if not json_data or language == "uz":
            return json_data
        
        translated_data = []
        for item in json_data:
            translated_item = item.copy()
            
            # Заменяем поля на переведенные версии
            for field in translatable_fields:
                lang_field = f"{field}_{language}"
                if lang_field in item and item[lang_field]:
                    translated_item[field] = item[lang_field]
                # Удаляем языковые поля из ответа
                for lang in ["uz", "ru", "en"]:
                    translated_item.pop(f"{field}_{lang}", None)
            
            translated_data.append(translated_item)
        
        return translated_data


class ContactPageSerializer(serializers.ModelSerializer):
    """Сериализатор для страницы контактов"""
    
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
        
        return representation


class SalesPointSerializer(serializers.ModelSerializer):
    """Сериализатор для торговой точки"""
    point_type = PointTypeSerializer(read_only=True)
    
    class Meta:
        model = SalesPoint
        fields = [
            "id",
            "name",
            "point_type",
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
                point_type_data = None
                if point.point_type:
                    point_type_name = getattr(point.point_type, f"name_{language}", point.point_type.name) if language != "uz" else point.point_type.name
                    point_type_data = {
                        "id": point.point_type.id,
                        "name": point_type_name,
                        "slug": point.point_type.slug,
                    }
                
                item = {
                    "id": point.id,
                    "name": getattr(point, f"name_{language}", point.name) if language != "uz" else point.name,
                    "point_type": point_type_data,
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
