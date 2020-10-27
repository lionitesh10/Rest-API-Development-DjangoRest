from rest_framework import serializers
from django.contrib.auth import get_user_model

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
