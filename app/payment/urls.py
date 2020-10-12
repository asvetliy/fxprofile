from django.urls import path
from . import views

urlpatterns = [
    path('payments/<payment>/<action>', views.PaymentURLDispatcher.as_view()),
]
