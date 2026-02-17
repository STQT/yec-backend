from django.urls import path
from apps.catalog.views import create_dealer_request

app_name = "catalog"

urlpatterns = [
    path('dealer-request/', create_dealer_request, name='dealer_request'),
]
