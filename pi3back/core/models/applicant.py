from django.db import models


class Applicant(models.Model):
    """Stores scraped LinkedIn profile data"""

    url = models.URLField(max_length=255, null=True, blank=True)
    about = models.TextField(blank=True, default="Carregando...")
    name = models.CharField(max_length=255, default="Carregando...")
    experiences = models.JSONField(default=list)
    educations = models.JSONField(default=list)
    interests = models.JSONField(default=list)
    accomplishments = models.JSONField(default=list)
    contacts = models.JSONField(default=list)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Applicant: {self.name}"

    class Meta:
        ordering = ["name"]
