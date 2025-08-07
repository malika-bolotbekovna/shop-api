from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.generics import CreateAPIView
from rest_framework import permissions
from django.contrib.auth import authenticate
from .serializers import UserRegisterSerializer, UserAuthSerializer, UserConfirmSerializer
from .models import ConfirmCode, CustomUser
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

        user = CustomUser.objects.create_user(
            email=email,
            password=password,
            is_active=False,
        )

        code = generate_code()
        ConfirmCode.objects.create(
            user=user, 
            code=code
        )
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

        serializer.confirm_instance.delete()
        return Response(
            data={'account is successfully activated'},
            status=status.HTTP_200_OK)