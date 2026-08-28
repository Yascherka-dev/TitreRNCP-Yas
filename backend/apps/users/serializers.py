from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError as DjangoValidationError
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from .models import User


class UserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        validators=[UniqueValidator(
            queryset=User.objects.all(),
            # Le message par défaut — « Un objet user avec ce champ email
            # existe déjà » — parle du modèle, pas à la personne.
            message="Un compte existe déjà avec cette adresse e-mail.",
        )],
    )
    password = serializers.CharField(write_only=True, min_length=8)

    class Meta:
        model = User
        fields = ['id', 'email', 'nom', 'prenom', 'role', 'date_inscription', 'password']
        read_only_fields = ['id', 'date_inscription', 'role']

    def validate(self, attrs):
        """
        Applique AUTH_PASSWORD_VALIDATORS, que le serializer ignorait jusqu'ici :
        « password » et « 12345678 » étaient acceptés.

        La validation a lieu ici, et non dans validate_password(), pour que
        UserAttributeSimilarityValidator puisse comparer le mot de passe à
        l'email, au nom et au prénom saisis.
        """
        attrs = super().validate(attrs)
        password = attrs.get('password')

        if password:
            candidat = User(
                email=attrs.get('email', ''),
                nom=attrs.get('nom', ''),
                prenom=attrs.get('prenom', ''),
            )
            try:
                validate_password(password, user=candidat)
            except DjangoValidationError as erreurs:
                raise serializers.ValidationError({'password': list(erreurs.messages)})

        return attrs

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)
