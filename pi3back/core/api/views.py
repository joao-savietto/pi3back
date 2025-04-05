from rest_framework import viewsets
from ..models import Occurrence, Classroom
from ...shared.permissions import IsProfessorOrReadOnly, IsSuperUserOrReadOnly
from django.contrib.auth import get_user_model

User = get_user_model()

from .serializers import (
    OccurrenceSerializer,
    ClassroomSerializer
)

from .filters import OccurrenceFilter

class OccurrenceViewSet(viewsets.ModelViewSet):
    queryset = Occurrence.objects.all()
    serializer_class = OccurrenceSerializer
    permission_classes = [IsProfessorOrReadOnly]
    filterset_class = OccurrenceFilter

    def get_queryset(self):
        qs = Occurrence.objects.all()
        if self.request.user.is_responsavel:
            children = User.objects.filter(responsavel = self.request.user).all()
            qs = qs.filter(student__in = children).all()
        return qs

class ClassroomViewSet(viewsets.ModelViewSet):
    serializer_class = ClassroomSerializer
    permission_classes = [IsSuperUserOrReadOnly]

    def get_queryset(self):
        user = self.request.user
        if user.is_superuser:
            return Classroom.objects.all().prefetch_related('members')
        return Classroom.objects.filter(members=user).prefetch_related('members')
