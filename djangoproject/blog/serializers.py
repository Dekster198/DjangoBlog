from rest_framework import serializers
from .models import *

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        extra_kwargs = {'date_joined': {'read_only': True}, 'last_login': {'read_only': True}}
        fields = ('id', 'email', 'username', 'password', 'first_name', 'last_name', 'is_superuser', 'is_staff',
                  'is_active', 'date_joined', 'last_login')

class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ('__all__')