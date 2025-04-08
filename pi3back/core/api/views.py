from rest_framework import viewsets
from django.contrib.auth import get_user_model
from pi3back.core.models.linkedin_profile import LinkedInProfile
from pi3back.core.api.serializers import LinkedInProfileSerializer
from drf_spectacular.utils import (
    extend_schema_view,
    extend_schema
)

User = get_user_model()


@extend_schema_view(
    list=extend_schema(
        description='Lista todos os perfis do LinkedIn cadastrados'
    ),
    retrieve=extend_schema(
        description='Retorna os detalhes de um perfil específico do LinkedIn'
    ),
    create=extend_schema(
        description='Cria um novo perfil do LinkedIn'
    ),
    partial_update=extend_schema(
        description='Atualiza parcialmente um perfil do LinkedIn'
    ),
    destroy=extend_schema(
        description='Remove um perfil do LinkedIn'
    )
)
class LinkedInProfileViewSet(viewsets.ModelViewSet):
    queryset = LinkedInProfile.objects.all()
    serializer_class = LinkedInProfileSerializer
    http_method_names = ['get', 'post', 'patch', 'delete']
