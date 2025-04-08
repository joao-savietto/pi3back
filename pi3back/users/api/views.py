from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework.viewsets import ModelViewSet
from django.contrib.auth import get_user_model
from rest_framework.decorators import action
from rest_framework.response import Response

from .serializers import UserSerializer

User = get_user_model()


@extend_schema_view(
    list=extend_schema(description='Lista todos os usuários'),
    retrieve=extend_schema(description='Recuperar um usuário por ID'),
    create=extend_schema(description='Criar um novo usuário'),
    update=extend_schema(description='Atualizar um usuário'),
    partial_update=extend_schema(
        description='Atualizar parcialmente um usuário'
    )
)
class UserViewSet(ModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    
    @action(detail=False, methods=['get'])
    def me(self, request):
        """Retorna os dados do usuário autenticado"""
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)
