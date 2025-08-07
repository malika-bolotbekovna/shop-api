from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from users.models import CustomUser
from .models import ConfirmCode

class UserBaseSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()



class UserRegisterSerializer(UserBaseSerializer):
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
        code = attrs.get("code")

        try:
            user = CustomUser.objects.get(id=user_id)
        except CustomUser.DoesNotExist:
            raise serializers.ValidationError({'user_id': 'User not found.'})

        try:
            confirm = ConfirmCode.objects.get(code=code, user=user)
        except ConfirmCode.DoesNotExist:
            raise serializers.ValidationError({'code': 'Invalid confirmation code for this user.'})

        self.user = user
        self.confirm_instance = confirm
        return attrs
    