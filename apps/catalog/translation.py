from modeltranslation.translator import register, TranslationOptions
from apps.catalog.models import (
    AboutPage,
    AdvantageCard,
    ContactPage,
    DealerAdvantage,
    FAQ,
    HomePage,
    News,
    NewsContentBlock,
    NewsImage,
    Region,
    SalesPoint,
)


@register(HomePage)
class HomePageTranslationOptions(TranslationOptions):
    """Настройки переводов для модели HomePage"""
    fields = ('title', 'description', 'collection_link', 'showroom_title', 'showroom_link')
    required_languages = ('uz',)  # Узбекский обязателен


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
    # Примечание: JSON поля (production_steps, company_history, production_capacity)
    # содержат переводы внутри себя в виде title_ru, title_en, description_ru, description_en и т.д.


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
    fields = ('text_content',)
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