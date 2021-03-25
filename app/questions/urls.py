from django.urls import path
from . import views

urlpatterns = [
    path('questions/ticket/create', views.CreateTicketView.as_view(), name='question-ticket-create'),
    path('questions/tickets', views.TicketsView.as_view(), name='question-tickets'),
    path('questions/<str:ticket>/<str:action>', views.TicketsURLDispatcher.as_view(), name='question-ticket-action'),
]
