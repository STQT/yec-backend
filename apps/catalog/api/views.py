from django.db.models import Count, Q
from django_filters import rest_framework as filters
from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import OpenApiParameter, extend_schema
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.filters import OrderingFilter
from rest_framework.mixins import CreateModelMixin, ListModelMixin, RetrieveModelMixin
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from apps.catalog.models import (
    AboutPage,
    AdvantageCard,
    Carpet,
    Collection,
    Color,
    ContactFormSubmission,
    ContactPage,
    FAQ,
    Gallery,
    HomePage,
    News,
    PointType,
    Region,
    Room,
    Style,
)

from .serializers import (
    AboutPageSerializer,
    AdvantageCardSerializer,
    CarpetDetailSerializer,
    CarpetListSerializer,
    CollectionDetailSerializer,
    CollectionListSerializer,
    ColorSerializer,
    ContactFormSubmissionSerializer,
    ContactPageSerializer,
    FAQSerializer,
    GallerySerializer,
    HomePageSerializer,
    NewsDetailSerializer,
    NewsListSerializer,
    PointTypeSerializer,
    RegionSerializer,
    RoomSerializer,
    StyleSerializer,
)

# OpenAPI параметр для языка
LANG_PARAMETER = OpenApiParameter(
    name="lang",
    type=OpenApiTypes.STR,
    location=OpenApiParameter.QUERY,
    description="Язык контента (uz, ru, en). По умолчанию: uz",
    required=False,
    enum=["uz", "ru", "en"],
)


class StandardResultsSetPagination(PageNumberPagination):
    """Пагинация для списков"""
    page_size = 12
    page_size_query_param = "page_size"
    max_page_size = 100


class CommaSeparatedMultipleChoiceFilter(filters.Filter):
    """Кастомный фильтр для значений через запятую"""
    
    def __init__(self, *args, **kwargs):
        self.to_field_name = kwargs.pop('to_field_name', 'slug')
        self.field_name = kwargs.pop('field_name')
        super().__init__(*args, **kwargs)
    
    def filter(self, qs, value):
        if not value:
            return qs
        
        # Разделяем значения по запятой
        values = [v.strip() for v in value.split(',') if v.strip()]
        if not values:
            return qs
        
        # Применяем фильтр напрямую через ManyToMany связь
        lookup = f"{self.field_name}__{self.to_field_name}__in"
        return qs.filter(**{lookup: values})


class CarpetFilter(filters.FilterSet):
    """Фильтр для ковров"""
    styles = CommaSeparatedMultipleChoiceFilter(
        field_name="styles",
        to_field_name="slug",
    )
    rooms = CommaSeparatedMultipleChoiceFilter(
        field_name="rooms",
        to_field_name="slug",
    )
    colors = CommaSeparatedMultipleChoiceFilter(
        field_name="colors",
        to_field_name="slug",
    )
    collection = filters.ModelChoiceFilter(
        field_name="collection",
        to_field_name="slug",
        queryset=Collection.objects.all(),
    )
    is_new = filters.BooleanFilter(field_name="is_new")
    is_popular = filters.BooleanFilter(field_name="is_popular")
    material = filters.CharFilter(field_name="material", lookup_expr="icontains")

    class Meta:
        model = Carpet
        fields = ["styles", "rooms", "colors", "collection", "is_new", "is_popular", "material"]


@extend_schema(tags=["Ковры"])
class CarpetViewSet(ListModelMixin, RetrieveModelMixin, GenericViewSet):
    """ViewSet для ковров"""
    queryset = Carpet.objects.filter(is_published=True).select_related("collection").prefetch_related(
        "styles", "rooms", "colors", "gallery_images"
    )
    pagination_class = StandardResultsSetPagination
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_class = CarpetFilter
    ordering_fields = ["created_at", "watched"]
    ordering = ["-created_at"]

    def get_serializer_class(self):
        if self.action == "retrieve":
            return CarpetDetailSerializer
        return CarpetListSerializer
    
    @extend_schema(parameters=[LANG_PARAMETER])
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
    
    @extend_schema(parameters=[LANG_PARAMETER])
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    def get_queryset(self):
        queryset = super().get_queryset()
        
        # Сортировка по новым/популярным
        sort_by = self.request.query_params.get("sort", None)
        if sort_by == "new":
            queryset = queryset.filter(is_new=True).order_by("-created_at")
        elif sort_by == "popular":
            queryset = queryset.filter(is_popular=True).order_by("-watched", "-created_at")
        
        return queryset

    @action(detail=True, methods=["post"])
    def increment_watch(self, request, pk=None):
        """Увеличить счетчик просмотров"""
        carpet = self.get_object()
        carpet.watched += 1
        carpet.save(update_fields=["watched"])
        return Response({"watched": carpet.watched}, status=status.HTTP_200_OK)

    @action(detail=False)
    def count(self, request):
        """Получить общее количество ковров"""
        count = self.get_queryset().count()
        return Response({"count": count}, status=status.HTTP_200_OK)


@extend_schema(tags=["Коллекции"])
class CollectionViewSet(ListModelMixin, RetrieveModelMixin, GenericViewSet):
    """ViewSet для коллекций"""
    queryset = Collection.objects.filter(is_published=True).annotate(
        carpets_count=Count("carpets", filter=Q(carpets__is_published=True))
    )
    lookup_field = "slug"

    def get_serializer_class(self):
        if self.action == "retrieve":
            return CollectionDetailSerializer
        return CollectionListSerializer
    
    @extend_schema(parameters=[LANG_PARAMETER])
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
    
    @extend_schema(parameters=[LANG_PARAMETER])
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @extend_schema(parameters=[LANG_PARAMETER])
    @action(detail=True, methods=["get"])
    def carpets(self, request, slug=None):
        """Получить ковры коллекции"""
        collection = self.get_object()
        carpets = Carpet.objects.filter(
            collection=collection, is_published=True
        ).select_related("collection").prefetch_related("styles", "rooms", "colors", "gallery_images")
        
        # Применяем фильтры из запроса
        filter_backend = DjangoFilterBackend()
        carpets = filter_backend.filter_queryset(request, carpets, CarpetViewSet())
        
        paginator = StandardResultsSetPagination()
        page = paginator.paginate_queryset(carpets, request)
        
        if page is not None:
            serializer = CarpetListSerializer(page, many=True, context={"request": request})
            return paginator.get_paginated_response(serializer.data)
        
        serializer = CarpetListSerializer(carpets, many=True, context={"request": request})
        return Response(serializer.data)


@extend_schema(tags=["Стили"])
class StyleViewSet(ListModelMixin, GenericViewSet):
    """ViewSet для стилей"""
    queryset = Style.objects.all()
    serializer_class = StyleSerializer
    pagination_class = None
    
    @extend_schema(parameters=[LANG_PARAMETER])
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)


@extend_schema(tags=["Комнаты"])
class RoomViewSet(ListModelMixin, GenericViewSet):
    """ViewSet для комнат"""
    queryset = Room.objects.all()
    serializer_class = RoomSerializer
    pagination_class = None
    
    @extend_schema(parameters=[LANG_PARAMETER])
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)


@extend_schema(tags=["Цвета"])
class ColorViewSet(ListModelMixin, GenericViewSet):
    """ViewSet для цветов"""
    queryset = Color.objects.all()
    serializer_class = ColorSerializer
    pagination_class = None
    
    @extend_schema(parameters=[LANG_PARAMETER])
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)


@extend_schema(tags=["Типы точек"])
class PointTypeViewSet(ListModelMixin, GenericViewSet):
    """ViewSet для типов точек"""
    queryset = PointType.objects.filter(is_published=True)
    serializer_class = PointTypeSerializer
    pagination_class = None
    
    @extend_schema(parameters=[LANG_PARAMETER])
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)


@extend_schema(tags=["Новости"])
class NewsViewSet(ListModelMixin, RetrieveModelMixin, GenericViewSet):
    """ViewSet для новостей"""
    queryset = News.objects.filter(is_published=True)
    pagination_class = StandardResultsSetPagination
    lookup_field = "slug"

    def get_serializer_class(self):
        if self.action == "retrieve":
            return NewsDetailSerializer
        return NewsListSerializer
    
    @extend_schema(parameters=[LANG_PARAMETER])
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
    
    @extend_schema(parameters=[LANG_PARAMETER])
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)


@extend_schema(tags=["Галерея"])
class GalleryViewSet(ListModelMixin, GenericViewSet):
    """ViewSet для галереи"""
    queryset = Gallery.objects.filter(is_published=True)
    serializer_class = GallerySerializer
    pagination_class = StandardResultsSetPagination
    
    @extend_schema(parameters=[LANG_PARAMETER])
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)


@extend_schema(tags=["Главная секция"])
class HomePageViewSet(ListModelMixin, GenericViewSet):
    """ViewSet для главной страницы"""
    queryset = HomePage.objects.filter(is_published=True)
    serializer_class = HomePageSerializer
    pagination_class = None
    
    @extend_schema(parameters=[LANG_PARAMETER])
    def list(self, request, *args, **kwargs):
        """Возвращает первый опубликованный объект главной страницы"""
        instance = self.get_queryset().first()
        if instance:
            serializer = self.get_serializer(instance)
            return Response(serializer.data)
        return Response({}, status=status.HTTP_200_OK)


@extend_schema(tags=["О компании"])
class AboutPageViewSet(ListModelMixin, GenericViewSet):
    """ViewSet для страницы о компании"""
    queryset = AboutPage.objects.filter(is_published=True)
    serializer_class = AboutPageSerializer
    pagination_class = None
    
    @extend_schema(parameters=[LANG_PARAMETER])
    def list(self, request, *args, **kwargs):
        """Возвращает первый опубликованный объект страницы о компании со всеми данными в одном запросе"""
        instance = self.get_queryset().first()
        if instance:
            serializer = self.get_serializer(instance)
            return Response(serializer.data)
        return Response({}, status=status.HTTP_200_OK)


@extend_schema(tags=["Контакты"])
class ContactPageViewSet(ListModelMixin, GenericViewSet):
    """ViewSet для страницы контактов"""
    queryset = ContactPage.objects.filter(is_published=True)
    serializer_class = ContactPageSerializer
    pagination_class = None
    
    @extend_schema(parameters=[LANG_PARAMETER])
    def list(self, request, *args, **kwargs):
        """Возвращает первый опубликованный объект страницы контактов"""
        instance = self.get_queryset().first()
        if instance:
            serializer = self.get_serializer(instance)
            return Response(serializer.data)
        return Response({}, status=status.HTTP_200_OK)


@extend_schema(tags=["Регионы и торговые точки"])
class RegionViewSet(ListModelMixin, GenericViewSet):
    """ViewSet для регионов с торговыми точками"""
    queryset = Region.objects.filter(is_published=True).prefetch_related('sales_points')
    serializer_class = RegionSerializer
    pagination_class = None
    lookup_field = "slug"
    
    @extend_schema(parameters=[LANG_PARAMETER])
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)


@extend_schema(tags=["Форма обратной связи"])
class ContactFormSubmissionViewSet(CreateModelMixin, GenericViewSet):
    """ViewSet для создания заявок (только POST)"""
    queryset = ContactFormSubmission.objects.all()
    serializer_class = ContactFormSubmissionSerializer
    
    def create(self, request, *args, **kwargs):
        """Создать новую заявку"""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        
        return Response(
            {"message": "Заявка успешно отправлена", "success": True},
            status=status.HTTP_201_CREATED
        )


@extend_schema(tags=["FAQ"])
class FAQViewSet(ListModelMixin, GenericViewSet):
    """ViewSet для FAQ"""
    queryset = FAQ.objects.filter(is_published=True)
    serializer_class = FAQSerializer
    pagination_class = None
    
    @extend_schema(parameters=[LANG_PARAMETER])
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)


@extend_schema(tags=["Преимущества"])
class AdvantageCardViewSet(ListModelMixin, GenericViewSet):
    """ViewSet для карточек преимуществ"""
    queryset = AdvantageCard.objects.filter(is_published=True)
    serializer_class = AdvantageCardSerializer
    pagination_class = None
    
    @extend_schema(parameters=[LANG_PARAMETER])
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)