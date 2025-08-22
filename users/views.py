from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.generics import CreateAPIView
from rest_framework import permissions
from django.contrib.auth import authenticate
from django.core.cache import cache
from .serializers import UserRegisterSerializer, UserAuthSerializer, UserConfirmSerializer, CustomTokenOptainSerializer
from .models import ConfirmCode, CustomUser
from rest_framework_simplejwt.views import TokenObtainPairView
import random



def generate_code():
    return f"{random.randint(0, 999999):06}"


class RegistrationAPIView(CreateAPIView):
    serializer_class = UserRegisterSerializer
    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data.get('email')
        password = serializer.validated_data.get('password')
        birthday = serializer.validated_data.get('birthday')

        user = CustomUser.objects.create_user(
            email=email,
            password=password,
            birthday=birthday,
            is_active=False,
        )

        code = generate_code()
        cache.set(f"confirm_code_{user.id}", code, timeout=300)
        print(f"CODE: {code}")

        return Response(
            data={
                'user_id': user.id,
                'confirmation_code': code},
            status=status.HTTP_201_CREATED
        )


class AuthAPIView(CreateAPIView):
    serializer_class = UserAuthSerializer
    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = authenticate(**serializer.validated_data)
        if user:
            token, _ = Token.objects.get_or_create(user=user)
            return Response(data={'key': token.key})
        return Response(
            status=status.HTTP_401_UNAUTHORIZED,
            data={'error': 'user credentials are wrong!'}
        )


class ConfirmationAPIView(CreateAPIView):
    serializer_class = UserConfirmSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.user
        user.is_active = True
        user.save()

        cache.delete(f"confirm_code_{user.id}")

        return Response(
            data={'account is successfully activated'},
            status=status.HTTP_200_OK)
    



class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenOptainSerializer