# Backend/core/views.py
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from .auth import create_user, authenticate_user

def _require_fields(data, *fields):
    missing = [f for f in fields if not data.get(f)]
    return missing

@api_view(["POST"])
def signup(request):
    missing = _require_fields(request.data, "username", "password")
    if missing:
        return Response(
            {"error": f"Missing fields: {', '.join(missing)}"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    ok, payload, err = create_user(request.data["username"], request.data["password"])
    if not ok:
        return Response({"error": err}, status=status.HTTP_409_CONFLICT)
    return Response(payload, status=status.HTTP_201_CREATED)

@api_view(["POST"])
def login(request):
    missing = _require_fields(request.data, "username", "password")
    if missing:
        return Response(
            {"error": f"Missing fields: {', '.join(missing)}"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    ok, payload, err = authenticate_user(request.data["username"], request.data["password"])
    if not ok:
        return Response({"error": err}, status=status.HTTP_401_UNAUTHORIZED)

    return Response(payload, status=status.HTTP_200_OK)
