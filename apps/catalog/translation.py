from modeltranslation.translator import register, TranslationOptions
from apps.catalog.models import (
    AboutPage,
    AdvantageCard,
    Carpet,
    Collection,
    Color,
    CompanyHistory,
    ContactPage,
    FAQ,
    HomePage,
    MainGallery,
    News,
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
        'cta_contact_link',
        'cta_dealer_link',
        # SEO поля
        'meta_title',
        'meta_description',
        'meta_keywords',
        'og_title',
        'og_description',
        'canonical_url',
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
        # Секция 1: О компании
        'about_section_title',
        'about_banner_title',
        'about_banner_subtitle',
        # Секция 2: Процесс производства
        'production_section_title',
        'production_title',
        # Секция 3: История компании
        'history_section_title',
        # Секция 4: Объемы производства
        'capacity_section_title',
        'capacity_title',
        'capacity_card_1_title',
        'capacity_card_1_subtitle',
        'capacity_card_2_title',
        'capacity_card_2_subtitle',
        'capacity_card_3_title',
        'capacity_card_3_subtitle',
        'capacity_card_4_title',
        'capacity_card_4_subtitle',
        # Секция 5: Партнерство для дилеров
        'dealer_section_title',
        'dealer_title',
        'dealer_card_1_title',
        'dealer_card_1_description',
        'dealer_card_2_title',
        'dealer_card_2_description',
        'dealer_card_3_title',
        'dealer_card_3_description',
        # SEO поля
        'meta_title',
        'meta_description',
        'meta_keywords',
        'og_title',
        'og_description',
        'canonical_url',
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
    fields = ('year_title', 'year_description')
    required_languages = ('uz',)


# ProductionCapacity и DealerAdvantage удалены - теперь статичные поля в AboutPage


@register(News)
class NewsTranslationOptions(TranslationOptions):
    """Настройки переводов для новостей"""
    fields = ('title', 'description', 'content')
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
        # SEO поля
        'meta_title',
        'meta_description',
        'meta_keywords',
        'og_title',
        'og_description',
        'canonical_url',
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