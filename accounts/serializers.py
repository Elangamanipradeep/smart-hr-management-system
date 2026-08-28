from django.contrib.auth.models import User, Group
from rest_framework import serializers


class HRUserSerializer(serializers.ModelSerializer):

    password = serializers.CharField(
        write_only=True,
        required=False,
    )

    role = serializers.SerializerMethodField(read_only=True)

    class Meta:

        model = User

        fields = [
            "id",
            "username",
            "first_name",
            "last_name",
            "email",
            "password",
            "is_active",
            "role",
        ]

        read_only_fields = [
            "id",
            "role",
        ]

    def get_role(self, obj):

        group = obj.groups.first()

        if group:
            return group.name

        return None

    def create(self, validated_data):

        password = validated_data.pop("password")

        user = User.objects.create_user(
            **validated_data,
            password=password,
        )

        hr_group, created = Group.objects.get_or_create(
            name="HR"
        )

        user.groups.add(hr_group)

        return user

    def update(self, instance, validated_data):

        password = validated_data.pop("password", None)

        for attr, value in validated_data.items():

            setattr(instance, attr, value)

        if password:

            instance.set_password(password)

        instance.save()

        return instance

class UserProfileSerializer(serializers.ModelSerializer):

    role = serializers.SerializerMethodField(read_only=True)

    class Meta:

        model = User

        fields = [
            "id",
            "username",
            "first_name",
            "last_name",
            "email",
            "role",
        ]

        read_only_fields = [
            "id",
            "username",
            "role",
        ]

    def get_role(self, obj):

        group = obj.groups.first()

        if group:
            return group.name

        return "User"

class ChangePasswordSerializer(serializers.Serializer):

    old_password = serializers.CharField(write_only=True)

    new_password = serializers.CharField(write_only=True)

    confirm_password = serializers.CharField(write_only=True)


class LogoutSerializer(serializers.Serializer):

    refresh = serializers.CharField()
