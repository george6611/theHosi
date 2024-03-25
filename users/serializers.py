from rest_framework import serializers
from .models import AdminUser

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdminUser
        fields = '__all__'