from django.db.models import Count, Q
from django_filters import rest_framework as filters
from django_filters.rest_framework import DjangoFilterBackend
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
    RegionSerializer,
    RoomSerializer,
    StyleSerializer,
)


class StandardResultsSetPagination(PageNumberPagination):
    """Пагинация для списков"""
    page_size = 12
    page_size_query_param = "page_size"
    max_page_size = 100


class CarpetFilter(filters.FilterSet):
    """Фильтр для ковров"""
    styles = filters.ModelMultipleChoiceFilter(
        field_name="styles__slug",
        to_field_name="slug",
        queryset=Style.objects.all(),
    )
    rooms = filters.ModelMultipleChoiceFilter(
        field_name="rooms__slug",
        to_field_name="slug",
        queryset=Room.objects.all(),
    )
    colors = filters.ModelMultipleChoiceFilter(
        field_name="colors__slug",
        to_field_name="slug",
        queryset=Color.objects.all(),
    )
    collection = filters.ModelChoiceFilter(
        field_name="collection__slug",
        to_field_name="slug",
        queryset=Collection.objects.all(),
    )
    is_new = filters.BooleanFilter(field_name="is_new")
    is_popular = filters.BooleanFilter(field_name="is_popular")
    material = filters.CharFilter(field_name="material", lookup_expr="icontains")

    class Meta:
        model = Carpet
        fields = ["styles", "rooms", "colors", "collection", "is_new", "is_popular", "material"]


class CarpetViewSet(ListModelMixin, RetrieveModelMixin, GenericViewSet):
    """ViewSet для ковров"""
    queryset = Carpet.objects.filter(is_published=True).select_related("collection").prefetch_related(
        "styles", "rooms", "colors"
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


class CollectionViewSet(ListModelMixin, RetrieveModelMixin, GenericViewSet):
    """ViewSet для коллекций"""
    queryset = Collection.objects.filter(is_published=True).select_related("type").annotate(
        carpets_count=Count("carpets", filter=Q(carpets__is_published=True))
    )
    lookup_field = "slug"

    def get_serializer_class(self):
        if self.action == "retrieve":
            return CollectionDetailSerializer
        return CollectionListSerializer

    @action(detail=True, methods=["get"])
    def carpets(self, request, slug=None):
        """Получить ковры коллекции"""
        collection = self.get_object()
        carpets = Carpet.objects.filter(
            collection=collection, is_published=True
        ).select_related("collection").prefetch_related("styles", "rooms", "colors")
        
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


class StyleViewSet(ListModelMixin, GenericViewSet):
    """ViewSet для стилей"""
    queryset = Style.objects.all()
    serializer_class = StyleSerializer
    pagination_class = None


class RoomViewSet(ListModelMixin, GenericViewSet):
    """ViewSet для комнат"""
    queryset = Room.objects.all()
    serializer_class = RoomSerializer
    pagination_class = None


class ColorViewSet(ListModelMixin, GenericViewSet):
    """ViewSet для цветов"""
    queryset = Color.objects.all()
    serializer_class = ColorSerializer
    pagination_class = None


class NewsViewSet(ListModelMixin, RetrieveModelMixin, GenericViewSet):
    """ViewSet для новостей"""
    queryset = News.objects.filter(is_published=True)
    pagination_class = StandardResultsSetPagination
    lookup_field = "slug"

    def get_serializer_class(self):
        if self.action == "retrieve":
            return NewsDetailSerializer
        return NewsListSerializer


class GalleryViewSet(ListModelMixin, GenericViewSet):
    """ViewSet для галереи"""
    queryset = Gallery.objects.filter(is_published=True)
    serializer_class = GallerySerializer
    pagination_class = StandardResultsSetPagination


class HomePageViewSet(ListModelMixin, GenericViewSet):
    """ViewSet для главной страницы"""
    queryset = HomePage.objects.filter(is_published=True)
    serializer_class = HomePageSerializer
    pagination_class = None
    
    def list(self, request, *args, **kwargs):
        """Возвращает первый опубликованный объект главной страницы"""
        instance = self.get_queryset().first()
        if instance:
            serializer = self.get_serializer(instance)
            return Response(serializer.data)
        return Response({}, status=status.HTTP_404_NOT_FOUND)


class AboutPageViewSet(ListModelMixin, GenericViewSet):
    """ViewSet для страницы о компании"""
    queryset = AboutPage.objects.filter(is_published=True)
    serializer_class = AboutPageSerializer
    pagination_class = None
    
    def list(self, request, *args, **kwargs):
        """Возвращает первый опубликованный объект страницы о компании со всеми данными в одном запросе"""
        instance = self.get_queryset().first()
        if instance:
            serializer = self.get_serializer(instance)
            return Response(serializer.data)
        return Response({}, status=status.HTTP_404_NOT_FOUND)


class ContactPageViewSet(ListModelMixin, GenericViewSet):
    """ViewSet для страницы контактов"""
    queryset = ContactPage.objects.filter(is_published=True)
    serializer_class = ContactPageSerializer
    pagination_class = None
    
    def list(self, request, *args, **kwargs):
        """Возвращает первый опубликованный объект страницы контактов"""
        instance = self.get_queryset().first()
        if instance:
            serializer = self.get_serializer(instance)
            return Response(serializer.data)
        return Response({}, status=status.HTTP_404_NOT_FOUND)


class RegionViewSet(ListModelMixin, GenericViewSet):
    """ViewSet для регионов с торговыми точками"""
    queryset = Region.objects.filter(is_published=True).prefetch_related('sales_points')
    serializer_class = RegionSerializer
    pagination_class = None
    lookup_field = "slug"


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


class FAQViewSet(ListModelMixin, GenericViewSet):
    """ViewSet для FAQ"""
    queryset = FAQ.objects.filter(is_published=True)
    serializer_class = FAQSerializer
    pagination_class = None


class AdvantageCardViewSet(ListModelMixin, GenericViewSet):
    """ViewSet для карточек преимуществ"""
    queryset = AdvantageCard.objects.filter(is_published=True)
    serializer_class = AdvantageCardSerializer
    pagination_class = None
