from django.urls import path

from . import views

urlpatterns = [
    path('', views.ProfileView.as_view(), name='profile-index'),
    path('change-profile', views.ChangeProfileView.as_view(), name='profile-change'),
    path('change-password', views.ChangePasswordView.as_view(), name='password-change'),
    path('web-terminal', views.WebTerminalView.as_view(), name='web-terminal'),
]
