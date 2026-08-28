from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.exceptions import ValidationError
from django.contrib.auth.models import User
from rest_framework.generics import (
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView,
)
from .permissions import IsAdmin


from .serializers import (
    UserProfileSerializer,
    ChangePasswordSerializer,
    LogoutSerializer,
    HRUserSerializer,
)

class HRUserListCreateAPIView(ListCreateAPIView):

    permission_classes = [
        IsAuthenticated,
        IsAdmin,
    ]

    serializer_class = HRUserSerializer

    queryset = (
        User.objects
        .filter(groups__name="HR")
        .order_by("-id")
        .distinct()
    )
    
class HRUserRetrieveUpdateDestroyAPIView(
    RetrieveUpdateDestroyAPIView
):

    permission_classes = [
        IsAuthenticated,
        IsAdmin,
    ]

    serializer_class = HRUserSerializer

    queryset = (
        User.objects
        .filter(groups__name="HR")
        .distinct()
    )

    def partial_update(self, request, *args, **kwargs):

        kwargs["partial"] = True

        return self.update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):

        user = self.get_object()

        user.is_active = not user.is_active

        user.save()

        if user.is_active:

            message = "HR account activated successfully."

        else:

            message = "HR account deactivated successfully."

        return Response(
            {
                "message": message,
            },
            status=status.HTTP_200_OK,
        )

@api_view(["GET", "PUT"])
@permission_classes([IsAuthenticated])
def profile_api(request):

    if request.method == "GET":

        serializer = UserProfileSerializer(request.user)

        return Response(serializer.data)

    serializer = UserProfileSerializer(
        request.user,
        data=request.data
    )

    if serializer.is_valid():

        serializer.save()

        return Response(
            serializer.data,
            status=status.HTTP_200_OK,
        )

    return Response(
        serializer.errors,
        status=status.HTTP_400_BAD_REQUEST,
    )

class ChangePasswordAPIView(APIView):

    permission_classes = [IsAuthenticated, IsAdmin,]

    def post(self, request):

        serializer = ChangePasswordSerializer(data=request.data)

        if serializer.is_valid():
            
            user = request.user
            
            old_password = serializer.validated_data["old_password"]
            new_password = serializer.validated_data["new_password"]
            confirm_password = serializer.validated_data["confirm_password"]
            
            if not user.check_password(old_password):
                return Response(
                    {
                        "error": "Old password is incorrect."
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            if new_password != confirm_password:
                return Response(
                    {
                        "error": "New password and confirm password do not match."
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            user.set_password(new_password)
            user.save()

            return Response(
                {
                    "message": "Password changed successfully."
                },
                status=status.HTTP_200_OK,
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )
        
class LogoutAPIView(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request):

        serializer = LogoutSerializer(data=request.data)

        serializer.is_valid(raise_exception=True)

        try:

            refresh_token = serializer.validated_data["refresh"]

            token = RefreshToken(refresh_token)

            token.blacklist()

            return Response(
                {
                    "message": "Logout successful."
                },
                status=status.HTTP_200_OK,
            )

        except Exception:

            raise ValidationError(
                {
                    "error": "Invalid refresh token."
                }
            )