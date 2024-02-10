from django.urls import include, path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view

from . import views


app_name = 'api'

urlpatterns = [
    # Product
    path("products/", views.ProductListApiView.as_view()),
]
