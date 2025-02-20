from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from .models import UserProfile


class BaseUserSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150, required=True)
    password = serializers.CharField(required=True)

class AuthSerializer(BaseUserSerializer):
    def validate(self, data):
        user = authenticate(username=data["username"], password=data["password"])
        if not user:
            raise serializers.ValidationError("Неверные учетные данные.")
        if not user.is_active:
            raise serializers.ValidationError("Пользователь не активирован.")
        data["user"] = user
        return data

class RegisterSerializer(BaseUserSerializer):
    class Meta:
        model = User
        fields = ("id", "username", "password")
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data, is_active=False)
        profile = UserProfile.objects.create(user=user)
        profile.generate_confirmation_code()
        return user

class ConfirmSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150, required=True)
    code = serializers.CharField(max_length=6)