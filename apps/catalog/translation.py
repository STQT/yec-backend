from modeltranslation.translator import register, TranslationOptions
from apps.catalog.models import (
    AboutPage,
    AdvantageCard,
    Carpet,
    Collection,
    Color,
    CompanyHistory,
    ContactPage,
    DealerAdvantage,
    FAQ,
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


@register(HomePage)
class HomePageTranslationOptions(TranslationOptions):
    """Настройки переводов для модели HomePage"""
    fields = (
        # Секция 1: Баннер
        'banner_title',
        'banner_description',
        'banner_link',
        'banner_showroom_title',
        'banner_showroom_link',
        # Секция 2: О нас
        'about_title',
        'about_link',
        'about_youtube_link',
        'about_bottom_description',
        # Секция 3: Шоурум
        'showroom_title',
        # Секция 4: Преимущества
        'advantage_title',
        'advantage_subtitle',
        'advantage_1_title',
        'advantage_1_description',
        'advantage_2_title',
        'advantage_2_description',
        'advantage_3_title',
        'advantage_3_description',
        'advantage_4_title',
        'advantage_4_description',
        # Секция 5: Призыв к действию
        'cta_title',
        'cta_description',
    )
    required_languages = ('uz',)  # Узбекский обязателен


@register(MainGallery)
class MainGalleryTranslationOptions(TranslationOptions):
    """Настройки переводов для нижней галереи"""
    fields = ("title",)
    required_languages = ("uz",)


@register(AboutPage)
class AboutPageTranslationOptions(TranslationOptions):
    """Настройки переводов для страницы о компании"""
    fields = (
        'company_title',
        'company_subtitle',
        'company_description',
        'production_section_title',
        'history_section_title',
        'capacity_section_title',
        'dealer_section_title',
        'showroom_button_text',
    )
    required_languages = ('uz',)


@register(ProductionStep)
class ProductionStepTranslationOptions(TranslationOptions):
    """Настройки переводов для этапов производства"""
    fields = ('title', 'description')
    required_languages = ('uz',)


@register(CompanyHistory)
class CompanyHistoryTranslationOptions(TranslationOptions):
    """Настройки переводов для истории компании"""
    fields = ('title', 'description')
    required_languages = ('uz',)


@register(ProductionCapacity)
class ProductionCapacityTranslationOptions(TranslationOptions):
    """Настройки переводов для объемов производства"""
    fields = ('capacity', 'description')
    required_languages = ('uz',)


@register(DealerAdvantage)
class DealerAdvantageTranslationOptions(TranslationOptions):
    """Настройки переводов для преимуществ дилеров"""
    fields = ('title', 'description')
    required_languages = ('uz',)


@register(News)
class NewsTranslationOptions(TranslationOptions):
    """Настройки переводов для новостей"""
    fields = ('title', 'description')
    required_languages = ('uz',)


@register(NewsContentBlock)
class NewsContentBlockTranslationOptions(TranslationOptions):
    """Настройки переводов для блоков контента новостей"""
    fields = ('title', 'text_content')
    required_languages = ('uz',)


@register(NewsImage)
class NewsImageTranslationOptions(TranslationOptions):
    """Настройки переводов для изображений новостей"""
    fields = ('caption',)
    required_languages = ('uz',)


@register(ContactPage)
class ContactPageTranslationOptions(TranslationOptions):
    """Настройки переводов для страницы контактов"""
    fields = (
        'page_title',
        'address_label',
        'address',
        'phone_label',
        'email_label',
        'form_title',
        'form_description',
    )
    required_languages = ('uz',)


@register(Region)
class RegionTranslationOptions(TranslationOptions):
    """Настройки переводов для регионов"""
    fields = ('name',)
    required_languages = ('uz',)


@register(SalesPoint)
class SalesPointTranslationOptions(TranslationOptions):
    """Настройки переводов для торговых точек"""
    fields = ('name', 'address', 'location')
    required_languages = ('uz',)


@register(FAQ)
class FAQTranslationOptions(TranslationOptions):
    """Настройки переводов для FAQ"""
    fields = ('question', 'answer')
    required_languages = ('uz',)


@register(AdvantageCard)
class AdvantageCardTranslationOptions(TranslationOptions):
    """Настройки переводов для карточек преимуществ"""
    fields = ('title', 'description')
    required_languages = ('uz',)


@register(Room)
class RoomTranslationOptions(TranslationOptions):
    """Настройки переводов для комнат"""
    fields = ('name',)
    required_languages = ('uz',)


@register(Style)
class StyleTranslationOptions(TranslationOptions):
    """Настройки переводов для стилей"""
    fields = ('name',)
    required_languages = ('uz',)


@register(Color)
class ColorTranslationOptions(TranslationOptions):
    """Настройки переводов для цветов"""
    fields = ('name',)
    required_languages = ('uz',)


@register(Collection)
class CollectionTranslationOptions(TranslationOptions):
    """Настройки переводов для коллекций"""
    fields = ('name', 'description')
    required_languages = ('uz',)


@register(Carpet)
class CarpetTranslationOptions(TranslationOptions):
    """Настройки переводов для характеристик ковра"""
    fields = ('code', 'material', 'density', 'base', 'pile_height', 'yarn_composition', 'weight')
    required_languages = ('uz',)