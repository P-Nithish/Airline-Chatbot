# Backend/core/views_chat.py
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from datetime import datetime
from .mongo import tickets, available_tickets

@api_view(["GET"])
def my_tickets(request):
    user_id = request.GET.get("user_id")
    if not user_id:
        return Response({"error": "user_id is required"}, status=status.HTTP_400_BAD_REQUEST)

    cursor = tickets.find(
        {"user_id": user_id, "Seat_status": "Booked"},
        {
            "_id": 0, "pnr": 1, "flight_id": 1, "src": 1, "dst": 1,
            "dep_time": 1, "arr_time": 1, "seat_no": 1,
            "current_departure": 1, "current_arrival": 1, "current_status": 1,
            "airline_name": 1, "user_id": 1, "Seat_status": 1,
        }
    )
    items = list(cursor)
    return Response({"tickets": items})

@api_view(["POST"])
def cancel_ticket(request):
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

    return Response({"message": "Cancelled successfully"})

@api_view(["POST"])
def seat_availability(request):
    """
    Returns: All documents with Seat_status='Available' matching given filters.
    """
    data = request.data or {}
    pnr          = (data.get("pnr") or "").strip().upper()
    flight_id    = (data.get("flight_id") or "").strip().upper()
    src          = (data.get("src") or "").strip().upper()
    dst          = (data.get("dst") or "").strip().upper()
    airline_name = (data.get("airline_name") or "").strip()

    if not any([pnr, flight_id, src, dst, airline_name]):
        return Response({
            "message": "Please provide one or more fields.",
            "required": {
                "pnr": "<string>  (e.g., RWQ248)",
                "flight_id": "<string> (e.g., LH0109)",
                "src": "<IATA>     (e.g., ATL)",
                "dst": "<IATA>     (e.g., MIA)",
                "airline_name": "<string> (e.g., Lufthansa)"
            },
            "hint": "You may provide any one or multiple fields."
        }, status=status.HTTP_400_BAD_REQUEST)

    query = {"Seat_status": "Available"}
    if pnr:       query["pnr"] = pnr
    if flight_id: query["flight_id"] = flight_id
    if src:       query["src"] = src
    if dst:       query["dst"] = dst
    if airline_name:
        # case-insensitive partial match
        query["airline_name"] = {"$regex": f"^{airline_name}", "$options": "i"}

    projection = {
        "_id": 0, "pnr": 1, "flight_id": 1, "src": 1, "dst": 1, "seat_no": 1,
        "dep_time": 1, "arr_time": 1, "current_departure": 1, "current_arrival": 1,
        "current_status": 1, "airline_name": 1, "Seat_status": 1
    }

    items = list(available_tickets.find(query, projection))
    return Response({"count": len(items), "seats": items}, status=status.HTTP_200_OK)


def _clean(s):
    return (s or "").strip()

def _upper(s):
    return _clean(s).upper()

@api_view(["POST"])
def flight_status(request):
    """
    returns current_status and a few details.
    """
    data = request.data or {}

    pnr          = _upper(data.get("pnr"))
    flight_id    = _upper(data.get("flight_id"))
    src          = _upper(data.get("src"))
    dst          = _upper(data.get("dst"))
    airline_name = _clean(data.get("airline_name"))

    if not any([pnr, flight_id, src, dst, airline_name]):
        return Response({
            "message": "Please provide one or more fields to check flight status.",
            "required": {
                "pnr": "<string> (e.g., RWQ248)",
                "flight_id": "<string> (e.g., LH0109)",
                "src": "<IATA> (e.g., ATL)",
                "dst": "<IATA> (e.g., MIA)",
                "airline_name": "<string> (e.g., Lufthansa)"
            },
            "hint": "You may provide any single field or a combination."
        }, status=status.HTTP_400_BAD_REQUEST)

    # Build a filter usable for both collections
    base = {}
    if pnr:       base["pnr"] = pnr
    if flight_id: base["flight_id"] = flight_id
    if src:       base["src"] = src
    if dst:       base["dst"] = dst
    if airline_name:
        base["airline_name"] = {"$regex": f"^{airline_name}", "$options": "i"}

    projection = {
        "_id": 0,
        "pnr": 1,
        "flight_id": 1,
        "airline_name": 1,
        "src": 1, "dst": 1,
        "dep_time": 1, "arr_time": 1,
        "current_departure": 1, "current_arrival": 1,
        "current_status": 1,
        "Seat_status": 1,
        "seat_no": 1
    }

    from_booked   = list(tickets.find(base, projection))
    from_inventory= list(available_tickets.find(base, projection))

    #deduplicate by (pnr or flight_id+seat_no) while keeping both separate
    def compact_name(doc):
        return doc.get("airline_name") or ""

    result = {
        "from_tickets": {
            "count": len(from_booked),
            "items": from_booked
        },
        "from_available_tickets": {
            "count": len(from_inventory),
            "items": from_inventory
        },
        "summary": {
            "matched_filters": {k: v for k, v in {
                "pnr": pnr, "flight_id": flight_id, "src": src, "dst": dst,
                "airline_name": airline_name
            }.items() if v}
        }
    }
    return Response(result, status=status.HTTP_200_OK)
