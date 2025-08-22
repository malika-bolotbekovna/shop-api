from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from users.models import CustomUser
from .models import ConfirmCode
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.core.cache import cache
class UserBaseSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()



class UserRegisterSerializer(UserBaseSerializer):
    birthday = serializers.DateField()
    def validate_username(self, email):
        try:
            CustomUser.objects.get('email=email')
        except CustomUser.DoesNotExist:
            return email
        raise ValidationError('Email already exists!')


class UserAuthSerializer(UserBaseSerializer):
    pass


class UserConfirmSerializer(serializers.Serializer):
    user_id = serializers.IntegerField()
    code = serializers.CharField(max_length=6)

    def validate(self, attrs):
        user_id = attrs.get("user_id")
        code_entered = attrs.get("code")

        try:
            user = CustomUser.objects.get(id=user_id)
        except CustomUser.DoesNotExist:
            raise serializers.ValidationError({'user_id': 'User not found.'})

        code_stored = cache.get(f"confirm_code_{user.id}")
        if code_stored is None:
            raise serializers.ValidationError({'code': 'Confirmation code expired or does not exist.'})

        if code_stored != code_entered:
            raise serializers.ValidationError({'code': 'Invalid confirmation code for this user.'})

        self.user = user
        return attrs



class CustomTokenOptainSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token["email"] = user.email
        token["birthday"] = str(user.birthday) if user.birthday else None
        return token
    


class GoogleLoginSerializer(serializers.Serializer):
    code = serializers.CharField()