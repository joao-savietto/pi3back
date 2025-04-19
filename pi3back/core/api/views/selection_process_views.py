from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from pi3back.shared.permissions import IsAuthenticated
from pi3back.core.models import SelectionProcess
from pi3back.core.api.serializers import (
    SelectionProcessSerializer,
    ApplicationSerializer
)
from drf_spectacular.utils import extend_schema_view, extend_schema

@extend_schema_view(
    list=extend_schema(description='Lista todos os processos seletivos'),
    retrieve=extend_schema(description='Recupera um processo seletivo por ID'),
    create=extend_schema(description='Cria um novo processo seletivo'),
    update=extend_schema(description='Atualiza um processo seletivo'),
    partial_update=extend_schema(description='Atualiza parcialmente um processo seletivo'),
    applications=extend_schema(description='Lista todas as aplicações de um processo seletivo')
)
class SelectionProcessViewSet(viewsets.ModelViewSet):
    queryset = SelectionProcess.objects.all()
    serializer_class = SelectionProcessSerializer
    permission_classes = [IsAuthenticated]

    @action(detail=True, methods=['get'])
    def applications(self, request, pk=None):
        selection_process = self.get_object()
        applications = selection_process.applications.all()
        serializer = ApplicationSerializer(applications, many=True)
        return Response(serializer.data)
