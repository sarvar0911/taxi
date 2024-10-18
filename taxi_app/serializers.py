from rest_framework import serializers
from .models import Order, User


class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['phone_number', 'role', 'full_name', 'gender', 'age', 'car_model', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class LoginSerializer(serializers.Serializer):
    phone_number = serializers.CharField()
    password = serializers.CharField(write_only=True)


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['id', 'customer', 'location_from', 'location_to', 'order_time', 'status', 'taxi_driver']
        read_only_fields = ['order_time', 'status', 'taxi_driver']


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['full_name', 'phone_number', 'gender', 'age', 'role', 'car_model']
