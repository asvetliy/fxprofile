from django.urls import path
# from django.conf.urls import url
# from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('verification', views.VerificationView.as_view(), name='verification'),
]
