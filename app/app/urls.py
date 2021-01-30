"""app URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.i18n import i18n_patterns
from django.conf.urls import url
from django.contrib.admin.views.decorators import staff_member_required
from django.views.static import serve
from django.conf import settings


@staff_member_required(login_url=settings.LOGIN_URL)
def protected_serve(request, path, document_root=None, show_indexes=False):
    return serve(request, path, document_root, show_indexes)


urlpatterns = [
    path('aZ0tD3wP8wZ0/', admin.site.urls),
    url(r'^%s(?P<path>.*)$' % settings.MEDIA_URL[1:], protected_serve, {'document_root': settings.MEDIA_ROOT}),
]
urlpatterns += i18n_patterns(
    path('', include('fxprofile.urls')),
    prefix_default_language=False
)
urlpatterns += i18n_patterns(
    path('', include('users.urls')),
    prefix_default_language=False
)
urlpatterns += i18n_patterns(
    path('', include('wallet.urls')),
    prefix_default_language=False
)
urlpatterns += i18n_patterns(
    path('', include('payment.urls')),
    prefix_default_language=False
)
urlpatterns += i18n_patterns(
    path('', include('mt4.urls')),
    prefix_default_language=False
)
urlpatterns += i18n_patterns(
    path('', include('verification.urls')),
    prefix_default_language=False
)
urlpatterns += i18n_patterns(
    path('i18n/', include('django.conf.urls.i18n')),
    prefix_default_language=False
)

admin.site.site_header = "Administration"
admin.site.site_title = "XYZ.TRADING"
# admin.site.index_title = "Administration"
