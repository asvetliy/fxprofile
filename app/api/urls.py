from django.urls import path

from . import views

urlpatterns = [
    path('api/symbols', views.PricesList.as_view(), name='api-symbols'),
]
