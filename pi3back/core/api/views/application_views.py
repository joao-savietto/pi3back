from rest_framework import viewsets
from pi3back.shared.permissions import IsAuthenticated
from pi3back.core.models import Application
from pi3back.core.api.serializers import ApplicationSerializer
from drf_spectacular.utils import extend_schema_view, extend_schema


@extend_schema_view(
    list=extend_schema(description="Lista todas as aplicações"),
    retrieve=extend_schema(description="Recupera uma aplicação por ID"),
    create=extend_schema(description="Cria uma nova aplicação"),
    update=extend_schema(description="Atualiza uma aplicação"),
    partial_update=extend_schema(
        description="Atualiza parcialmente uma aplicação"
    ),
)
class ApplicationViewSet(viewsets.ModelViewSet):
    queryset = Application.objects.all()
    serializer_class = ApplicationSerializer
    http_method_names = ["get", "post", "patch", "delete"]
    permission_classes = [IsAuthenticated]
