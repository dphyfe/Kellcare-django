from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework import status
from django.contrib.auth import authenticate


@api_view(["GET"])
@permission_classes([])  # No permission required
def cors_test(request):
    """
    CORS test endpoint - should work from any origin
    GET /api/cors-test/
    """
    return Response(
        {
            "message": "CORS is working!",
            "timestamp": "2025-10-23T12:38:50Z",
            "method": request.method,
            "origin": request.headers.get("Origin", "No origin header"),
            "user_agent": request.headers.get("User-Agent", "No user agent"),
        }
    )


@api_view(["POST"])
@permission_classes([])  # No permission required for getting token
def get_auth_token(request):
    """
    Get or create authentication token for user

    POST /api/auth/token/
    {
        "username": "your_username",
        "password": "your_password"
    }
    """
    username = request.data.get("username")
    password = request.data.get("password")

    if not username or not password:
        return Response({"error": "Username and password required"}, status=status.HTTP_400_BAD_REQUEST)

    user = authenticate(username=username, password=password)

    if user:
        token, created = Token.objects.get_or_create(user=user)
        return Response({"token": token.key, "user_id": user.id, "username": user.username, "message": "Token created" if created else "Token retrieved"})
    else:
        return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def refresh_auth_token(request):
    """
    Refresh (regenerate) authentication token for authenticated user

    Requires Authorization: Token <your_token>
    POST /api/auth/refresh-token/
    """
    try:
        # Delete old token
        Token.objects.filter(user=request.user).delete()

        # Create new token
        token = Token.objects.create(user=request.user)

        return Response({"token": token.key, "user_id": request.user.id, "username": request.user.username, "message": "Token refreshed successfully"})
    except Exception:
        return Response({"error": "Failed to refresh token"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_user_info(request):
    """
    Get current user information

    Requires Authorization: Token <your_token>
    GET /api/auth/user/
    """
    return Response(
        {
            "user_id": request.user.id,
            "username": request.user.username,
            "email": request.user.email,
            "first_name": request.user.first_name,
            "last_name": request.user.last_name,
            "is_staff": request.user.is_staff,
            "is_superuser": request.user.is_superuser,
        }
    )
