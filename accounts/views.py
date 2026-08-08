from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.exceptions import ValidationError


from .serializers import (
    RegisterSerializer,
    UserProfileSerializer,
    ChangePasswordSerializer,
    LogoutSerializer,
)

@api_view(["POST"])
@permission_classes([AllowAny])
def register_api(request):
    
    serializer = RegisterSerializer(data=request.data)
    
    if serializer.is_valid():
        
        serializer.save()
        
        return Response(
            {
                "message": "User registered successfully.",
                "data": serializer.data,
            },
            status=status.HTTP_201_CREATED,
        )
        
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def profile_api(request):
    
    serializer = UserProfileSerializer(request.user)
    
    return Response(serializer.data)


class ChangePasswordAPIView(APIView):

    permission_classes = [IsAuthenticated]

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