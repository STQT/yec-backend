from django.urls import path
from rest_framework.routers import DefaultRouter

from .views import (
    AboutPageViewSet,
    AdvantageCardViewSet,
    CarpetViewSet,
    CollectionViewSet,
    ColorViewSet,
    ContactFormSubmissionViewSet,
    ContactPageViewSet,
    FAQViewSet,
    GalleryViewSet,
    HomePageViewSet,
    NewsViewSet,
    PointTypeViewSet,
    RegionViewSet,
    RoomViewSet,
    StyleViewSet,
)

router = DefaultRouter()
router.register("carpets", CarpetViewSet, basename="carpet")
router.register("collections", CollectionViewSet, basename="collection")
router.register("styles", StyleViewSet, basename="style")
router.register("rooms", RoomViewSet, basename="room")
router.register("colors", ColorViewSet, basename="color")
router.register("point-types", PointTypeViewSet, basename="point-type")
router.register("news", NewsViewSet, basename="news")
router.register("gallery", GalleryViewSet, basename="gallery")
router.register("homepage", HomePageViewSet, basename="homepage")
router.register("about", AboutPageViewSet, basename="about")
router.register("contact", ContactPageViewSet, basename="contact")
router.register("regions", RegionViewSet, basename="region")
router.register("contact-form", ContactFormSubmissionViewSet, basename="contact-form")
router.register("faq", FAQViewSet, basename="faq")
router.register("advantages", AdvantageCardViewSet, basename="advantage")

app_name = "catalog_api"
urlpatterns = router.urls
