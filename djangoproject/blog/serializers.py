from rest_framework import serializers
from django.contrib.auth.hashers import make_password
from .models import *

class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ('__all__')

    def get_fields(self):
        fields = super().get_fields()
        request = self.context.get('request', None)

        if not request.user.is_staff:
            fields['user'] = serializers.HiddenField(default=User.objects.get(username=request.user.username))

        return fields


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        extra_kwargs = {'date_joined': {'read_only': True}, 'last_login': {'read_only': True}}
        fields = ('id', 'email', 'username', 'password', 'first_name', 'last_name', 'is_superuser', 'is_staff',
                  'is_active', 'date_joined', 'last_login')

    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data.get('password'))
        user = User.objects.create(**validated_data)
        photo = 'static/images/avatar/default/default_img.jpg'
        Account.objects.create(user=user, photo=photo)

        return user

class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        extra_kwargs = {'slug': {'read_only': True}}
        fields = ('__all__')

    def get_fields(self):
        fields = super().get_fields()
        request = self.context.get('request', None)
        if not request.user.is_staff:
            fields['author'] = serializers.HiddenField(default=Account.objects.get(user=request.user))

        return fields

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        extra_kwargs = {'author': {'read_only': True}}
        fields = ('__all__')

    def get_fields(self):
        fields = super().get_fields()
        request = self.context.get('request', None)
        fields['author'] = serializers.CharField(default=Account.objects.get(user=request.user))
        if not request.user.is_staff:
            fields['author'] = serializers.HiddenField(default=Account.objects.get(user=request.user))

        return fields