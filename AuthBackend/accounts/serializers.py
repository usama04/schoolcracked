from djoser.serializers import UserCreateSerializer
from django.contrib.auth import get_user_model
from rest_framework import serializers


User = get_user_model()

class UserCreateSerializer(UserCreateSerializer):
    password = serializers.CharField(write_only=True)
    
    class Meta(UserCreateSerializer.Meta):
        model = User
        fields = ("id", "email", "first_name", "last_name", "company_name", "location", "is_teacher", "profile_pic_url", "birth_date", "password", "is_active", "is_staff")