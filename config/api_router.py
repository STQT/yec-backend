from django.conf import settings
from rest_framework.routers import DefaultRouter
from rest_framework.routers import SimpleRouter

from apps.catalog.api.urls import router as catalog_router
from apps.users.api.views import UserViewSet

router = DefaultRouter() if settings.DEBUG else SimpleRouter()

router.register("users", UserViewSet)

# Включаем эндпоинты каталога
router.registry.extend(catalog_router.registry)


app_name = "api"
urlpatterns = router.urls
