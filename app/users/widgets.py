from urllib import parse as urlparse
from django.utils.safestring import mark_safe
from django.utils.html import escape

from django_countries.widgets import CountrySelectWidget, COUNTRY_CHANGE_HANDLER
from django_countries.conf import settings as widget_settings


class MyCountrySelectWidget(CountrySelectWidget):
    def render(self, name, value, attrs=None, renderer=None):
        from django_countries.fields import Country

        attrs = attrs or {}
        widget_id = attrs and attrs.get("id")
        if widget_id:
            flag_id = f"flag_{widget_id}"
            attrs["onchange"] = COUNTRY_CHANGE_HANDLER % urlparse.urljoin(
                widget_settings.STATIC_URL, widget_settings.COUNTRIES_FLAG_URL
            ) + ' $(this).valid();'
        else:
            flag_id = ""
        widget_render = super(CountrySelectWidget, self).render(name, value, attrs, renderer=renderer)
        if isinstance(value, Country):
            country = value
        else:
            country = Country(value or "__")
        with country.escape:
            return mark_safe(  # nosec
                self.layout.format(
                    widget=widget_render, country=country, flag_id=escape(flag_id)
                )
            )