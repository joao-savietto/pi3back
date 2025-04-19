from django.contrib.auth import get_user_model
from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import status, viewsets

from pi3back.core.models import Applicant
from pi3back.core.api.serializers import ApplicantSerializer
from pi3back.core.services.celery_tasks import scrape_and_update_applicant
from pi3back.shared.permissions import IsAuthenticated

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
