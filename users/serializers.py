from rest_framework import serializers
from .models import CustomUser

class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'email', 'password', 'is_staff', 'is_active', 'date_joined']
        read_only_fields = ['id', 'is_staff', 'is_active', 'date_joined']

    def create(self, validated_data):
        user = CustomUser.objects.create_user(email=validated_data['email'], preferred_name=validated_data['preferred_name'])
        return user

    def update(self, instance, validated_data):
        instance.email = validated_data.get('email', instance.email)
        instance.preferred_name = validated_data.get('preferred_name', instance.preferred_name)
        instance.save()
        return instance
