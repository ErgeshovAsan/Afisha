from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .serializers import RegisterSerializer, AuthSerializer, ConfirmSerializer
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User


@api_view(['POST'])
def authorization_api_view(request):
    serializer = AuthSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    user = serializer.validated_data["user"]

    if user:
        token, _ = Token.objects.get_or_create(user=user)
        return Response(data={'key': token.key})
    return Response(status=status.HTTP_401_UNAUTHORIZED)

@api_view(['POST'])
def registration_api_view(request):
    serializer = RegisterSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    user = serializer.save()

    return Response(
        {"user_id": user.id, "username": user.username, "confirmation_code": user.userprofile.confirmation_code},
        status=status.HTTP_201_CREATED,
    )

@api_view(['POST'])
def confirm_api_view(request):
    serializer = ConfirmSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    try:
        user = User.objects.get(username=serializer.validated_data["username"])
        profile = user.userprofile

        if profile.confirmation_code == serializer.validated_data["code"]:
            user.is_active = True
            profile.confirmation_code = None
            user.save()
            profile.save()
            return Response({"message": "Регистрация подтверждена!"}, status=status.HTTP_200_OK)
        else:
            return Response({"error": "Неверный код подтверждения."}, status=status.HTTP_400_BAD_REQUEST)

    except User.DoesNotExist:
        return Response({"error": "Пользователь не найден."}, status=status.HTTP_404_NOT_FOUND)
