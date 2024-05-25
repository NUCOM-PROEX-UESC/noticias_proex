from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import UserType

User = get_user_model()

class UserTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserType
        fields = ['id', 'name']

class UserSerializer(serializers.ModelSerializer):
    user_types = UserTypeSerializer(many=True, read_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'full_name', 'matricula', 'email', 'user_types']

class RegisterSerializer(serializers.ModelSerializer):
    user_types = serializers.PrimaryKeyRelatedField(many=True, queryset=UserType.objects.all())

    class Meta:
        model = User
        fields = ['username', 'password', 'full_name', 'matricula', 'email', 'user_types']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user_types = validated_data.pop('user_types', [])
        user = User.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password'],
            full_name=validated_data['full_name'],
            matricula=validated_data['matricula'],
            email=validated_data['email']
        )
        user.user_types.set(user_types)
        user.save()
        return user
