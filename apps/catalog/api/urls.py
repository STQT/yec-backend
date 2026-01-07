from django.urls import path
from rest_framework.routers import DefaultRouter

from .views import (
    CarpetViewSet,
    CollectionViewSet,
    ColorViewSet,
    GalleryViewSet,
    NewsViewSet,
    RoomViewSet,
    StyleViewSet,
)

router = DefaultRouter()
router.register("carpets", CarpetViewSet, basename="carpet")
router.register("collections", CollectionViewSet, basename="collection")
router.register("styles", StyleViewSet, basename="style")
router.register("rooms", RoomViewSet, basename="room")
router.register("colors", ColorViewSet, basename="color")
router.register("news", NewsViewSet, basename="news")
router.register("gallery", GalleryViewSet, basename="gallery")

app_name = "catalog_api"
urlpatterns = router.urls
