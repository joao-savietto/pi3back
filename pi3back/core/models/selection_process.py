from django.db import models
from enum import Enum


class ProcessCategory(Enum):
    ADMINISTRATIVE_FINANCIAL = 'administrative_financial'
    COMMERCIAL = 'commercial'
    COMMUNICATION_MARKETING = 'communication_marketing'
    DEVELOPMENT = 'development'
    INNOVATION = 'innovation'
    PEOPLE = 'people'
    PRODUCTS = 'products'
    OPERATIONS = 'operations'
    QUALITY = 'quality'

    @classmethod
    def choices(cls):
        return [(key.value, key.name.replace('_', ' ').title()) for key in cls]


class SelectionProcess(models.Model):
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    ended_at = models.DateTimeField(null=True, blank=True)
    is_ended = models.BooleanField(default=False)
    category = models.CharField(
        max_length=50,
        choices=ProcessCategory.choices(),
        default=ProcessCategory.DEVELOPMENT.value
    )

    def __str__(self):
        return f"Selection Process: {self.description[:50]}"

    class Meta:
        verbose_name_plural = "Selection Processes"
        ordering = ['-created_at', 'category', 'is_ended']
