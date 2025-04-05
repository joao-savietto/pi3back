from rest_framework import serializers
from django.contrib.auth import get_user_model

from pi3back.occurrences.api.serializers import ClassroomSerializer
from pi3back.occurrences.models.classroom import Classroom

User = get_user_model()

from typing import TypedDict, List

class UserTypedDict(TypedDict):
    email: str
    nome: str
    is_professor: bool
    is_aluno: bool
    is_responsavel: bool
    responsavel: dict  

class CommonUserValidation:
    def validate(self, data):
        roles = [data.get('is_professor', False), data.get('is_aluno', False), data.get('is_responsavel', False)]
        if sum(roles) > 1:
            raise serializers.ValidationError("A user cannot have more than one role.")
        return data    

class CreateUserSerializer(CommonUserValidation, serializers.ModelSerializer):

    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['id', 'nome', 'email', 'is_professor', 'is_aluno', 'is_responsavel', 'password', 'responsavel']

    def create(self, validated_data):
        user = User(**validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user
    
class UpdateUserSerializer(CommonUserValidation, serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['id', 'nome', 'email', 'is_professor', 'is_aluno', 'is_responsavel', 'responsavel']

    
class GetUserSerializer(CommonUserValidation, serializers.ModelSerializer):
    responsavel = serializers.SerializerMethodField()
    classroom = serializers.SerializerMethodField(read_only=True)

    def get_responsavel(self, obj) -> List[UserTypedDict]:
        if obj.responsavel:
            return self.to_representation(obj.responsavel)
        return None
    
    def get_classroom(self, obj):
        try:
            user_classroom = Classroom.objects.filter(members=obj).all()
            user_classroom = ClassroomSerializer(user_classroom, many=True).data
            return user_classroom
        except Classroom.DoesNotExist:
            return None

    class Meta:
        model = User
        fields = ['id', 'nome', 'email', 'is_professor', 'is_aluno', 'is_responsavel', 'is_superuser', 'responsavel', 'classroom']

