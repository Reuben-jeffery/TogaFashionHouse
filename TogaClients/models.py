from django.db import models
from django.core.validators import RegexValidator
from auditlog.registry import auditlog

class Client(models.Model):
    """
    Core CRM Database Entity Model representing elite atelier client portfolios.
    """
    
    # Modernized Gender Constant Choice Configuration Elements
    class GenderOptions(models.TextChoices):
        MALE = 'M', 'Male'
        FEMALE = 'F', 'Female'
        UNSPECIFIED = 'U', 'Unspecified'

    name = models.CharField(
        max_length=100,
        db_index=True # Direct field acceleration lookup injection optimization
    )
    
    phone = models.CharField(
        max_length=20,
        unique=True,
        validators=[
            RegexValidator(
                regex=r'^\+?\d{7,15}$', # Adjusted structural baseline limit down to 7 to safely map international variations
                message="Enter a valid normalized identity phone digits sequence format."
            )
        ]
    )
    
    gender = models.CharField(
        max_length=1,
        choices=GenderOptions.choices,
        default=GenderOptions.UNSPECIFIED,
        blank=True,
        null=True
    )
    
    # Audit trail execution pipelines tracking timestamps parameters
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    last_order_date = models.DateField(blank=True, null=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Client Profile"
        verbose_name_plural = "Client Profiles"
        indexes = [
            models.Index(fields=["phone"], name="client_phone_lookup_idx"),
            models.Index(fields=["name"], name="client_name_lookup_idx"),
        ]

    def __str__(self):
        return f"{self.name} — ({self.phone})"

# Register client audit monitoring trace line hooks
auditlog.register(Client)