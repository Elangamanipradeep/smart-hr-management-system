from django.contrib.auth.models import User
from rest_framework import serializers


class RegisterSerializer(serializers.ModelSerializer):
    
    password = serializers.CharField(write_only=True)
    
    class Meta:
        model = User
        fields = [
            "first_name",
            "last_name",
            "username",
            "email",
            "password",
        ]
        
    def create(self, validated_data):
        
        user = User.objects.create_user(
            first_name=validated_data["first_name"],
            last_name=validated_data["last_name"],
            username=validated_data["username"],
            email=validated_data["email"],
            password=validated_data["password"],
        )
        
        return user
    
    
class UserProfileSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "first_name",
            "last_name",
            "email",
        ]
        
class ChangePasswordSerializer(serializers.Serializer):
      
    old_password = serializers.CharField(write_only=True)
    
    new_password = serializers.CharField(write_only=True)
    
    confirm_password = serializers.CharField(write_only=True)
    

class LogoutSerializer(serializers.Serializer):
    
    refresh = serializers.CharField()