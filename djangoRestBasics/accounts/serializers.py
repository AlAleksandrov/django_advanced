from django.contrib.auth import get_user_model
from rest_framework import serializers

UserModel = get_user_model()

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=128, write_only=True)

    class Meta:
        model = UserModel
        fields = ['username', 'password', 'email']

    def create(self, validated_data):
        user = UserModel.objects.create_user(
            username=validated_data.get('username'),
            password=validated_data.get('password'),
            email=validated_data.get('email'),
        )
        return user