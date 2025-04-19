from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "nome", "email", "linkedin_user", "linkedin_password"]
        extra_kwargs = {
            "password": {"write_only": True},
            "linkedin_user": {"required": False},
            "linkedin_password": {"required": False},
        }

    def create(self, validated_data):
        user = User.objects.create_user(
            email=validated_data["email"],
            nome=validated_data["nome"],
            password=validated_data["password"],
        )
        return user

    def update(self, instance, validated_data):
        instance.email = validated_data.get("email", instance.email)
        instance.nome = validated_data.get("nome", instance.nome)
        instance.linkedin_user = validated_data.get(
            "linkedin_user", instance.linkedin_user
        )
        instance.linkedin_password = validated_data.get(
            "linkedin_password", instance.linkedin_password
        )

        if "password" in validated_data:
            instance.set_password(validated_data["password"])

        instance.save()
        return instance
