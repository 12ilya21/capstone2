from django.contrib.auth.models import User # User 모델
from django.contrib.auth.password_validation import validate_password # Django의 기본 pw 검증 도구
from django.contrib.auth import authenticate

from rest_framework import serializers
from rest_framework.authtoken.models import Token # Token 모델

from .models import User

# 회원가입 시리얼라이저
class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True,
        required=True,
        validators=[validate_password], # 비밀번호에 대한 검증
    )

    class Meta:
        model = User
        fields = ('username', 'password', 'language')

    def create(self, validated_data):
        # CREATE 요청에 대해 create 메서드를 오버라이딩하여, 유저를 생성하고 토큰도 생성하게 해준다.
        user = User.objects.create_user(
            username=validated_data['username'],
            language=validated_data['language'],
        )

        user.set_password(validated_data['password'])
        user.save()
        token = Token.objects.create(user=user)
        return user

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True, write_only=True)
    
    def validate(self, data):
        user = authenticate(**data)
        if user:
            return user
        raise serializers.ValidationError(
            {"error": "Unable to log in with provided credentials."}
        )
