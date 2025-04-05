from django.db import models

class Occurrence(models.Model):

    ATIVIDADE_NAO_ENTREGUE = 'ATIVIDADE_NAO_ENTREGUE'
    ATRASO_NA_ENTREGA = 'ATRASO_NA_ENTREGA'
    MAU_COMPORTAMENTO = 'MAU_COMPORTAMENTO'
    FALTOU_AULA = 'FALTOU_AULA'
    CHEGOU_ATRASADO = 'CHEGOU_ATRASADO'
    OUTRO = 'OUTRO'

    OCCURRENCE_CHOICES = [
        (ATIVIDADE_NAO_ENTREGUE, 'Atividade não entregue'),
        (ATRASO_NA_ENTREGA, 'Atraso na entrega'),
        (MAU_COMPORTAMENTO, 'Mau comportamento'),
        (FALTOU_AULA, 'Faltou aula'),
        (CHEGOU_ATRASADO, 'Chegou atrasado'),
        (OUTRO, 'Outro'),
    ]

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name='teacher_occurrences')
    viewed_at = models.DateTimeField(null=True, blank=True)
    is_viewed = models.BooleanField(default=False)
    description = models.TextField(blank=True, default='')
    occurrence_type = models.CharField(max_length=255, choices=OCCURRENCE_CHOICES, default=OUTRO)
    student = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name='student_occurrences')

    class Meta:
        ordering = ['-created_at']
