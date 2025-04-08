from django.db import models
from enum import Enum


class ProcessCategory(Enum):
    DEVELOPER = 'developer'
    SALES = 'sales'
    MARKETING = 'marketing'
    MANAGEMENT = 'management'
    QUALITY_ASSURANCE = 'quality_assurance'
    IT_INFRA = 'it_infra'

    @classmethod
    def choices(cls):
        return [(key.value, key.name.replace('_', ' ').title()) for key in cls]


class SelectionProcess(models.Model):
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    ended_at = models.DateTimeField(null=True, blank=True)
    is_ended = models.BooleanField(default=False)
    category = models.CharField(
        max_length=20,
        choices=ProcessCategory.choices(),
        default=ProcessCategory.DEVELOPER.value
    )

    def __str__(self):
        return f"Selection Process: {self.description[:50]}"

    class Meta:
        verbose_name_plural = "Selection Processes"
        ordering = ['-created_at']
