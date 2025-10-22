# Backend/core/views_chat.py
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from datetime import datetime
from .mongo import tickets

@api_view(["GET"])
def my_tickets(request):
    user_id = request.GET.get("user_id")
    if not user_id:
        return Response({"error": "user_id is required"}, status=status.HTTP_400_BAD_REQUEST)

    cursor = tickets.find(
        {"user_id": user_id, "Seat_status": "Booked"},
        {
            "_id": 0,
            "pnr": 1,
            "flight_id": 1,
            "src": 1,
            "dst": 1,
            "dep_time": 1,
            "arr_time": 1,
            "seat_no": 1,
            "current_departure": 1,
            "current_arrival": 1,
            "current_status": 1,
            "airline_name": 1,
            "user_id": 1,
            "Seat_status": 1,
        }
    )
    items = list(cursor)
    return Response({"tickets": items})

@api_view(["POST"])
def cancel_ticket(request):
    """
    POST /chat/cancel/
    Body: { "user_id": "CUS000001", "flight_id": "LH0100", "seat_no": "9B" }
    Action: Only cancel if currently Seat_status='Booked' for this user.
            After cancel: Seat_status='Cancelled', user_id=null
    """
    user_id   = request.data.get("user_id")
    flight_id = request.data.get("flight_id")
    seat_no   = request.data.get("seat_no")

    if not (user_id and flight_id and seat_no):
        return Response({"error": "user_id, flight_id, seat_no are required"}, status=status.HTTP_400_BAD_REQUEST)

    res = tickets.update_one(
        {"user_id": user_id, "flight_id": flight_id, "seat_no": seat_no, "Seat_status": "Booked"},
        {"$set": {
            "Seat_status": "Cancelled",
            "user_id": None,
            "cancelled_at": datetime.utcnow(),
            "updated_at": datetime.utcnow(),
        }}
    )

    if res.matched_count == 0:
        return Response({"error": "Ticket not found or already cancelled"}, status=status.HTTP_404_NOT_FOUND)

    # No price column in your data; return a generic message or compute later if you add price
    return Response({"message": "Cancelled successfully"})
