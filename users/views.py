from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from .serializers import UserRegisterSerializer, UserAuthSerializer, UserConfirmSerializer
from .models import ConfirmCode
import random



def generate_code():
    return f"{random.randint(0, 999999):06}"


@api_view(['POST'])
def registration_api_view(request):
    serializer = UserRegisterSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    username = serializer.validated_data.get('username')
    password = serializer.validated_data.get('password')

    user = User.objects.create_user(
        username=username,
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
        data={'user_id': user.id},
        status=status.HTTP_201_CREATED
    )


@api_view(['POST'])
def authorization_api_view(request):
    serializer = UserAuthSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    user = authenticate(**serializer.validated_data)
    if user:
        token, _ = Token.objects.get_or_create(user=user)
        return Response(data={'key': token.key})
    return Response(
        status=status.HTTP_401_UNAUTHORIZED,
        data={'error': 'user credentials are wrong!'}
    )

@api_view(['POST'])
def confirmation_api_view(request):

    serializer = UserConfirmSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    user = serializer.user
    user.is_active = True
    user.save()

    serializer.confirm_instance.delete()
    return Response(status=status.HTTP_200_OK)