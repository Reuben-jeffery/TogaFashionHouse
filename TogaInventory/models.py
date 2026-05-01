from django.db import models
from django.utils import timezone
from TogaClients.models import Client
from auditlog.registry import auditlog
from django.contrib.auth.models import User


class Inventory(models.Model):
    """
    Represents inventory records tied to a client.
    Tracks materials, payments, and staff accountability.
    """

    # 🔗 Link to Client
    client = models.ForeignKey(
        Client,
        on_delete=models.CASCADE,
        related_name="inventories",
        help_text="The client this inventory record belongs to"
    )

    # Material details
    description = models.TextField(
        verbose_name="Material Description",
        help_text="Details of the material selected or brought"
    )
    date_of_registration = models.DateField(
        default=timezone.now,
        verbose_name="Date of Registration"
    )

    # Contact (optional, since client already has phone)
    phone = models.CharField(
        max_length=20,
        blank=True,
        null=True,
        verbose_name="Phone Number",
        help_text="Optional contact number for this inventory record"
    )

    # Financials
    amount_charged = models.DecimalField(
        max_digits=12, decimal_places=2,
        verbose_name="Amount Charged"
    )
    amount_deposited = models.DecimalField(
        max_digits=12, decimal_places=2,
        default=0,
        verbose_name="Amount Deposited"
    )
    deposit_date = models.DateField(
        blank=True, null=True,
        verbose_name="Deposit Date"
    )
    balance = models.DecimalField(
        max_digits=12, decimal_places=2,
        default=0,
        verbose_name="Balance"
    )

    # Payment status
    paid_fully = models.BooleanField(
        default=False,
        verbose_name="Paid Fully?"
    )
    paid_fully_date = models.DateField(
        blank=True, null=True,
        verbose_name="Paid Fully Date"
    )

    # Collection and staff accountability
    collection_date = models.DateField(
        blank=True, null=True,
        verbose_name="Collection Date"
    )
    received_by = models.CharField(
        max_length=150,
        blank=True, null=True,
        verbose_name="Received By"
    )
    cleared_by = models.CharField(
        max_length=150,
        blank=True, null=True,
        verbose_name="Cleared By"
    )

    # Worker who created this record
    created_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Created By",
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
        verbose_name = "Inventory"
        verbose_name_plural = "Inventories"

    def __str__(self):
        status = "Paid Fully" if self.paid_fully else "Partially Paid"
        return f"{self.client.name} - {self.description[:30]}... ({status})"

    def update_deposit_summary(self):
        """
        Recalculate deposits and balance whenever a new deposit is added.
        """
        total = sum(d.amount for d in self.deposits.all())
        self.amount_deposited = total
        self.balance = self.amount_charged - total

        if self.balance <= 0:
            self.paid_fully = True
            if not self.paid_fully_date:
                self.paid_fully_date = timezone.now()
        else:
            self.paid_fully = False
            self.paid_fully_date = None

        self.save()


class Deposit(models.Model):
    """
    Represents a single deposit/payment made toward an inventory record.
    Allows tracking of multiple installments.
    """
    inventory = models.ForeignKey(
        Inventory,
        on_delete=models.CASCADE,
        related_name="deposits"
    )
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    date = models.DateField(default=timezone.now)
    received_by = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.inventory.client} - ₦{self.amount} on {self.date}"


# 🔒 Track changes with auditlog
auditlog.register(Inventory)
