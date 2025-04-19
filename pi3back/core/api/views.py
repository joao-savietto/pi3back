from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from pi3back.shared.permissions import IsAuthenticated
from pi3back.core.models import Applicant, SelectionProcess, Application
from pi3back.core.api.serializers import (
    ApplicantSerializer,
    SelectionProcessSerializer,
    ApplicationSerializer,
)
from pi3back.core.services.celery_tasks import scrape_and_update_applicant
from drf_spectacular.utils import extend_schema_view, extend_schema

User = get_user_model()


@extend_schema_view(
    list=extend_schema(description="Lista todos os candidatos cadastrados"),
    retrieve=extend_schema(
        description="Retorna os detalhes de um candidato específico"
    ),
    create=extend_schema(description="Cria um novo candidato"),
    partial_update=extend_schema(
        description="Atualiza parcialmente um candidato"
    ),
    destroy=extend_schema(description="Remove um candidato"),
)
class ApplicantViewSet(viewsets.ModelViewSet):
    queryset = Applicant.objects.all()
    serializer_class = ApplicantSerializer
    http_method_names = ["get", "post", "patch", "delete"]
    permission_classes = [IsAuthenticated]

    def _trigger_scraper(self, applicant):
        user = self.request.user
        if user.linkedin_user and user.linkedin_password and applicant.url:
            scrape_and_update_applicant.delay(
                linkedin_url_profile=applicant.url,
                username=user.linkedin_user,
                password=user.linkedin_password,
                applicant_id=applicant.id,
            )

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        if response.status_code == status.HTTP_201_CREATED:
            applicant = Applicant.objects.get(id=response.data["id"])
            self._trigger_scraper(applicant)
        return response

    def update(self, request, *args, **kwargs):
        response = super().update(request, *args, **kwargs)
        if response.status_code == status.HTTP_200_OK:
            applicant = self.get_object()
            self._trigger_scraper(applicant)
        return response

    def partial_update(self, request, *args, **kwargs):
        response = super().partial_update(request, *args, **kwargs)
        if response.status_code == status.HTTP_200_OK:
            applicant = self.get_object()
            self._trigger_scraper(applicant)
        return response


@extend_schema_view(
    list=extend_schema(description="Lista todos os processos seletivos"),
    retrieve=extend_schema(
        description="Recupera um processo seletivo por ID"
    ),
    create=extend_schema(description="Cria um novo processo seletivo"),
    update=extend_schema(description="Atualiza um processo seletivo"),
    partial_update=extend_schema(
        description="Atualiza parcialmente um processo seletivo"
    ),
    applications=extend_schema(
        description="Lista todas as aplicações de um processo seletivo"
    ),
)
class SelectionProcessViewSet(viewsets.ModelViewSet):
    queryset = SelectionProcess.objects.all()
    serializer_class = SelectionProcessSerializer
    permission_classes = [IsAuthenticated]

    @action(detail=True, methods=["get"])
    def applications(self, request, pk=None):
        selection_process = self.get_object()
        applications = selection_process.applications.all()
        serializer = ApplicationSerializer(applications, many=True)
        return Response(serializer.data)


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
