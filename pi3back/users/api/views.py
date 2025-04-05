from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework.viewsets import ModelViewSet
from django.contrib.auth import get_user_model
from rest_framework import status


from pi3back.occurrences.api.filters import UserFilter

from .serializers import CreateUserSerializer, UpdateUserSerializer, GetUserSerializer
from ...shared.permissions import IsAuthenticated

User = get_user_model()

from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Q

@extend_schema_view(
    list=extend_schema(description='Lista todos os usuários', summary='Obter lista de usuários'),
    retrieve=extend_schema(description='Recuperar um usuário por ID', summary='Obter um usuário específico'),
    create=extend_schema(description='Criar um usuário', summary='Criar uma nova conta de usuário'),
    update=extend_schema(description='Atualizar um usuário', summary='Atualizar detalhes de um usuário existente'),
    partial_update=extend_schema(description='Atualizar parcialmente um usuário', summary='Atualizar alguns campos de um usuário existente'),
    me=extend_schema(description='Recuperar o usuário logado', summary='Obter detalhes do usuário logado'),
    children=extend_schema(description='Listar usuários filhos do usuário lugado', summary='Listar usuários filhos do usuário lugado'),
    teachers=extend_schema(description='Listar usuários professores', summary='Listar de usuários professores'),
    parents=extend_schema(description='Listar usuários pais', summary='Listar de usuários pais'),
    students=extend_schema(description='Listar usuários alunos', summary='Listar de usuários alunos'),
)
class UserViewSet(ModelViewSet):
    serializer_class = CreateUserSerializer
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated]
    filterset_class = UserFilter    

    def get_queryset(self):
        qs = User.objects.all()
        if self.request.user.is_responsavel:
            qs = qs.filter(Q(responsavel = self.request.user) | Q(pk=self.request.user.pk)).all()
        return qs    

    def get_serializer(self, *args, **kwargs):
        if self.action == 'create':
            return CreateUserSerializer(*args, **kwargs)
        if self.action == 'update' or self.action == 'partial_update':
            return UpdateUserSerializer(*args, **kwargs)
        return GetUserSerializer(*args, **kwargs)
    
    @action(detail=False, methods=['get'])
    def me(self, request):
        current_user = request.user
        serializer = GetUserSerializer(current_user)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def children(self, request, pk=None):
        user = request.user
        if user.is_responsavel == False:
            return Response({'detail': 'Apenas usuários pais podem listar os seus filhos'}, status=status.HTTP_403_FORBIDDEN)
        children = User.objects.filter(responsavel=user).all()
        serializer = GetUserSerializer(children, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def teachers(self, request):
        user = request.user
        if user.is_superuser == False:
            return Response({'detail': 'Apenas usuários administradores podem listar os professores'}, status=status.HTTP_403_FORBIDDEN)
        teachers = User.objects.filter(is_professor=True).all()
        serializer = GetUserSerializer(teachers, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def parents(self, request):
        user = request.user
        if user.is_superuser == False:
            return Response({'detail': 'Apenas usuários administradores podem listar os pais'}, status=status.HTTP_403_FORBIDDEN)
        parents = User.objects.filter(is_responsavel=True).all()
        serializer = GetUserSerializer(parents, many=True)
        return Response(serializer.data)


    @action(detail=False, methods=['get'])
    def students(self, request):
        user = request.user
        if user.is_superuser == False:
            return Response({'detail': 'Apenas usuários administradores podem listar os alunos'}, status=status.HTTP_403_FORBIDDEN)
        students = User.objects.filter(is_aluno=True).all()
        serializer = GetUserSerializer(students, many=True)
        return Response(serializer.data)
        
    