from django.urls import path
from . import views
from django.views.decorators.csrf import csrf_exempt


urlpatterns = [
    path('payments/<payment>/<action>', csrf_exempt(views.PaymentURLDispatcher.as_view())),
]
