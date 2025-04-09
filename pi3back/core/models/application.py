from django.db import models
from enum import Enum


class ApplicationStep(Enum):
    HR_INTERVIEW = "HR Interview"
    TECHNICAL_CHALLENGE = "Technical Challenge"
    LEADERSHIP_INTERVIEW = "Leadership Interview"
    TECHNICAL_CHALLENGE_NOT_SUBMITTED = "Technical Challenge Not Submitted"
    REJECTED = "Rejected"
    DECLINED = "Declined"
    OFFER_PHASE = "Offer Phase"
    ONBOARDING = "Onboarding"
    HUNTING = "Hunting"
    DATABASE = "Database"
    STAND_BY = "Stand By"


class Application(models.Model):
    applicant = models.ForeignKey(
        "Applicant",
        on_delete=models.CASCADE,
        related_name="applications"
    )
    selection_process = models.ForeignKey(
        "SelectionProcess",
        on_delete=models.CASCADE,
        related_name="applications"
    )
    current_step = models.CharField(
        max_length=50,
        choices=[(step.value, step.value) for step in ApplicationStep],
        default=ApplicationStep.HR_INTERVIEW.value
    )

    class Meta:
        unique_together = ('applicant', 'selection_process')

    def __str__(self):
        return f"{self.applicant} - {self.selection_process}"
