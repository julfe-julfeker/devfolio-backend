
from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError as DjangoValidationError

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny

from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError

from rest_framework_simplejwt.views import TokenRefreshView
from rest_framework.permissions import IsAuthenticated


from .permissions import IsOwner


class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        username = request.data.get("username", "")
        password = request.data.get("password", "")

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if not user or not user.is_active or not user.is_superuser:
            return Response(
                {"detail": "Invalid credentials."},
                status=status.HTTP_401_UNAUTHORIZED
            )

        refresh = RefreshToken.for_user(user)

        return Response({
            "access": str(refresh.access_token),
            "refresh": str(refresh),
            "user": {
                "id": user.id,
                "username": user.username,
                "email": user.email,
                "is_superuser": user.is_superuser,
            }
        })


class MeView(APIView):
    permission_classes = [IsOwner]

    def get(self, request):
        user = request.user

        return Response({
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "is_superuser": user.is_superuser,
        })


class LogoutView(APIView):
    permission_classes = [IsOwner]

    def post(self, request):
        refresh_token = request.data.get("refresh")

        if not refresh_token:
            return Response(
                {"detail": "Refresh token is required."},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            token = RefreshToken(refresh_token)

            if str(token["user_id"]) != str(request.user.id):
                return Response(
                    {"detail": "Invalid refresh token."},
                    status=status.HTTP_400_BAD_REQUEST
                )

            token.blacklist()

        except TokenError:
            return Response(
                {"detail": "Invalid or expired refresh token."},
                status=status.HTTP_400_BAD_REQUEST
            )

        return Response({"detail": "Logged out successfully."})


class ChangePasswordView(APIView):
    permission_classes = [IsOwner]

    def post(self, request):
        user = request.user
        old_password = request.data.get("old_password", "")
        new_password = request.data.get("new_password", "")

        if not user.check_password(old_password):
            return Response(
                {"old_password": ["Incorrect password."]},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            validate_password(new_password, user)
        except DjangoValidationError as error:
            return Response(
                {"new_password": error.messages},
                status=status.HTTP_400_BAD_REQUEST
            )

        user.set_password(new_password)
        user.save(update_fields=["password"])

        return Response({
            "detail": "Password changed successfully."
        })



class OwnerTokenRefreshView(TokenRefreshView):
    pass