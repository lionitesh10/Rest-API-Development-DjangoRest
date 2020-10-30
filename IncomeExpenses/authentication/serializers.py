from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate
from rest_framework.exceptions import AuthenticationFailed
User=get_user_model()

class RegisterSerializer(serializers.ModelSerializer):
    password=serializers.CharField(max_length=64,min_length=8,write_only=True)
    class Meta:
        model=User
        fields=['email','username','password']
    def validate(self, attrs):
        username=attrs.get('username','')
        email=attrs.get('email','')
        if not username.isalnum():
            raise serializers.ValidationError("Username should be alphanumeric ")
        return attrs

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)

class EmailVerificationSerializer(serializers.ModelSerializer):
    token=serializers.CharField(max_length=555)
    class Meta:
        model=User
        fields=['token']

class LoginSerializer(serializers.ModelSerializer):
    email=serializers.EmailField(max_length=255,min_length=3)
    password=serializers.CharField(max_length=68,min_length=8,write_only=True)
    username=serializers.CharField(max_length=255,min_length=3,read_only=True)
    tokens=serializers.CharField(max_length=555,read_only=True)

    class Meta:
        model=User
        fields=['email','password','username','tokens']

    def validate(self, attrs):
        email=attrs.get('email','')
        password=attrs.get('password','')

        user=authenticate(email=email,password=password)
        if not user:
            raise AuthenticationFailed('Invalid Credentials Provided !! ')
        if not user.is_active:
            raise AuthenticationFailed('Sorry the account is deactivated.! Contact the site ')
        if not user.is_verified:
            raise AuthenticationFailed('Please Verify your email to continue !!! ')

        return {
            'email':user.email,
            'username':user.username,
            'tokens':user.tokens()
        }
