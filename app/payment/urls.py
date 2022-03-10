from django.urls import path
from django.views.decorators.csrf import csrf_exempt

from . import views


urlpatterns = [
    path('payments/<payment>/<action>', csrf_exempt(views.PaymentURLDispatcher.as_view())),
]
