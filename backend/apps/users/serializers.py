from rest_framework import serializers
from .models import User


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)

    class Meta:
        model = User
        fields = ['id', 'email', 'nom', 'prenom', 'role', 'date_inscription', 'password']
        read_only_fields = ['id', 'date_inscription', 'role']

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)
