from django.contrib.auth.models import User
from djoser.serializers import UserSerializer, UserCreatePasswordRetypeSerializer


class UserUpdateSerializer(UserSerializer):

    class Meta:
        model = User
        fields = '__all__'


class UsersCreateSerializer(UserCreatePasswordRetypeSerializer):

    class Meta:
        model = User
        fields = ('username', 'password')
