from django.contrib.auth import get_user_model, authenticate
from rest_framework import serializers

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    def create(self, validated_data):
        user = super().create(validated_data)
        user.set_password(validated_data['password'])
        user.is_active = True
        user.save()
        return user

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'email', 'password')
        extra_kwargs = {
            'password': {'write_only': True, 'min_length': 8},
            'email': {'required': True},
            'first_name': {'required': True},
            'last_name': {'required': True},
        }
