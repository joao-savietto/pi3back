from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()


class CommonUserValidation:
    def validate(self, data):
        roles = [
            data.get("is_professor", False),
            data.get("is_aluno", False),
            data.get("is_responsavel", False),
        ]
        if sum(roles) > 1:
            raise serializers.ValidationError("A user cannot have more than one role.")
        return data


class CreateUserSerializer(CommonUserValidation, serializers.ModelSerializer):

    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = [
            "id",
            "nome",
            "email",
            "is_professor",
            "is_aluno",
            "is_responsavel",
            "password",
            "responsavel",
            "linkedin_user",
            "linkedin_password",
        ]

    def create(self, validated_data):
        user = User(**validated_data)
        user.set_password(validated_data["password"])
        user.save()
        return user


class UpdateUserSerializer(CommonUserValidation, serializers.ModelSerializer):

    class Meta:
        model = User
        fields = "__all__"


class GetUserSerializer(CommonUserValidation, serializers.ModelSerializer):

    class Meta:
        model = User
        fields = "__all__"
