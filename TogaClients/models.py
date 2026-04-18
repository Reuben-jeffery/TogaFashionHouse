from django.db import models
from django.core.validators import RegexValidator
from django.contrib.auth.models import User
from auditlog.registry import auditlog

class Client(models.Model):
    name = models.CharField(max_length=100)
    phone = models.CharField(
        max_length=20,
        unique=True,
        validators=[RegexValidator(r'^\+?\d{9,15}$', "Enter a valid phone number.")]
    )
    gender = models.CharField(
        max_length=1,
        choices=[('M', 'Male'), ('F', 'Female')],
        blank=True,
        null=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    last_order_date = models.DateField(blank=True, null=True)

    class Meta:
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["phone"]),
            models.Index(fields=["name"]),
        ]

    def __str__(self):
        return f"{self.name} ({self.phone})"

# Register only Client here
auditlog.register(Client)
auditlog.register(User)
