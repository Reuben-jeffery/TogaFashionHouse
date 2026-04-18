from django.db import models
from django.utils import timezone
from TogaClients.models import Client
from auditlog.registry import auditlog
from django.contrib.auth.models import User

class Inventory(models.Model):
    """
    Represents inventory records tied to a client.
    Each record tracks materials, payments, and staff accountability.
    """
    # 🔗 Link to Client
    client = models.ForeignKey(
        Client,
        on_delete=models.CASCADE,
        related_name="inventories",  # lets you do client.inventories.all()
        help_text="The client this inventory record belongs to"
    )

    # Material details
    description = models.TextField(
        help_text="Details of the material selected or brought"
    )
    date_of_registration = models.DateField(default=timezone.now)

    # Contact (optional, since client already has phone)
    phone = models.CharField(
        max_length=20,
        blank=True,
        null=True,
        help_text="Optional contact number for this inventory record"
    )

    # Financials
    amount_charged = models.DecimalField(max_digits=10, decimal_places=2)
    amount_deposited = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    deposit_date = models.DateField(blank=True, null=True)
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    # Payment status
    paid_fully = models.BooleanField(default=False)
    paid_fully_date = models.DateField(blank=True, null=True)

    # Collection and staff accountability
    collection_date = models.DateField(blank=True, null=True)
    received_by = models.CharField(max_length=150, blank=True, null=True)
    cleared_by = models.CharField(max_length=150, blank=True, null=True)

     # Worker who created this record
    created_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        help_text="The worker who created this inventory record"
    )
    
    # Audit timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["client"]),
            models.Index(fields=["paid_fully"]),
        ]

    def __str__(self):
        status = "Paid Fully" if self.paid_fully else "Partially Paid"
        return f"{self.client.name} - {self.description[:30]}... ({status})"

# 🔒 Track changes with auditlog
auditlog.register(Inventory)
