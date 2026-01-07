from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class CatalogConfig(AppConfig):
    name = "apps.catalog"
    verbose_name = _("Catalog")

    def ready(self):
        """
        Override this method in subclasses to run code when Django starts.
        """
