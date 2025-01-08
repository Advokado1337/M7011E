from rest_framework import serializers
from django.contrib.auth.models import User

class UserRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('email','password')

    def create(self, validated_data):
        validated_data['username'] = validated_data['email']
        auth_user = User.objects.create_user(**validated_data)
        return auth_user

class UsersSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'password', 'email']