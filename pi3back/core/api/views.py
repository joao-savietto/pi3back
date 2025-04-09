from rest_framework import viewsets
from django.contrib.auth import get_user_model
from pi3back.shared.permissions import UserPermissions
from pi3back.core.models import Applicant, SelectionProcess, Application
from pi3back.core.api.serializers import (
    ApplicantSerializer,
    SelectionProcessSerializer,
    ApplicationSerializer
)
from drf_spectacular.utils import (
    extend_schema_view,
    extend_schema
)

User = get_user_model()


@extend_schema_view(
    list=extend_schema(
        description='Lista todos os candidatos cadastrados'
    ),
    retrieve=extend_schema(
        description='Retorna os detalhes de um candidato específico'
    ),
    create=extend_schema(
        description='Cria um novo candidato'
    ),
    partial_update=extend_schema(
        description='Atualiza parcialmente um candidato'
    ),
    destroy=extend_schema(
        description='Remove um candidato'
    )
)
class ApplicantViewSet(viewsets.ModelViewSet):
    queryset = Applicant.objects.all()
    serializer_class = ApplicantSerializer
    http_method_names = ['get', 'post', 'patch', 'delete']
    permission_classes = [UserPermissions]


@extend_schema_view(
    list=extend_schema(description='Lista todos os processos seletivos'),
    retrieve=extend_schema(description='Recupera um processo seletivo por ID'),
    create=extend_schema(description='Cria um novo processo seletivo'),
    update=extend_schema(description='Atualiza um processo seletivo'),
    partial_update=extend_schema(
        description='Atualiza parcialmente um processo seletivo'
    )
)
class SelectionProcessViewSet(viewsets.ModelViewSet):
    queryset = SelectionProcess.objects.all()
    serializer_class = SelectionProcessSerializer


@extend_schema_view(
    list=extend_schema(description='Lista todas as aplicações'),
    retrieve=extend_schema(description='Recupera uma aplicação por ID'),
    create=extend_schema(description='Cria uma nova aplicação'),
    update=extend_schema(description='Atualiza uma aplicação'),
    partial_update=extend_schema(
        description='Atualiza parcialmente uma aplicação'
    )
)
class ApplicationViewSet(viewsets.ModelViewSet):
    queryset = Application.objects.all()
    serializer_class = ApplicationSerializer
    http_method_names = ['get', 'post', 'patch', 'delete']
