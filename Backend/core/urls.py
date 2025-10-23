
from django.urls import path
from .views import signup, login
from .views_chat import my_tickets, cancel_ticket, seat_availability, flight_status, ask_policy

urlpatterns = [
    path("auth/signup/", signup, name="signup"),
    path("auth/login/",  login,  name="login"),
    path("chat/my-tickets/", my_tickets, name="my_tickets"),
    path("chat/cancel/",     cancel_ticket, name="cancel_ticket"),
    path("chat/seat-availability/", seat_availability, name="seat_availability"),
    path("chat/flight-status/",     flight_status, name="flight_status"), 
    path("chat/ask-policy/", ask_policy, name="ask_policy"),
]

