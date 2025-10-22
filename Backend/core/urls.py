
from django.urls import path
from .views import signup, login
from .views_chat import my_tickets, cancel_ticket

urlpatterns = [
    path("auth/signup/", signup, name="signup"),
    path("auth/login/",  login,  name="login"),
    path("chat/my-tickets/", my_tickets, name="my_tickets"),
    path("chat/cancel/",     cancel_ticket, name="cancel_ticket"),
]
