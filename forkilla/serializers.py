from .models import Restaurant
from rest_framework import serializers
from django.contrib.auth.models import User

class RestaurantSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Restaurant
        fields = (
        'restaurant_number', 'name', 'menu_description', 
        'price_average', 'is_promot', 'rate', 'address', 
        'city', 'country', 'featured_photo', 'category', 
        'capacity')

class UsersSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = (
            'username', 'first_name', 'last_name', 
        'email', 'password', 'groups', 'user_permissions', 
        'is_staff', 'is_active', 'is_superuser', 'last_login', 
        'date_joined'
        )

class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = (
            'username', 'first_name', 'last_name', 
        'email', 'password', 'groups', 'user_permissions', 
        'is_staff', 'is_active', 'is_superuser', 'last_login', 
        'date_joined'
        )

class PasswordSerializer(serializers.HyperlinkedModelSerializer):
    new_password = serializers.CharField(required=True)

