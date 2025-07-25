from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from django.contrib.auth.models import User
from .models import ConfirmCode

class UserBaseSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150)
    password = serializers.CharField()



class UserRegisterSerializer(UserBaseSerializer):
    def validate_username(self, username):
        try:
            User.objects.get('username=username')
        except:
            return username
        raise ValidationError('User already exists!')


class UserAuthSerializer(UserBaseSerializer):
    pass


class UserConfirmSerializer(serializers.Serializer):
    code = serializers.CharField(max_length=6)

    def validate_code(self, code):
        try:
            confirm = ConfirmCode.objects.get(code=code)
        except ConfirmCode.DoesNotExist:
            raise serializers.ValidationError('Invalid confirmation code!')
        
        self.user = confirm.user
        self.confirm_instance = confirm
        return code
    