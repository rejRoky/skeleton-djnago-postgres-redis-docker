from rest_framework import serializers
from .models import User

class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for user profile management.
    """
    class Meta:
        model = User
        fields = ['id', 'mobile_number', 'first_name', 'last_name', 'email']
