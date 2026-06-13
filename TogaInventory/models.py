from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.db.models import Sum
from decimal import Decimal
from TogaClients.models import Client
from auditlog.registry import auditlog

class Inventory(models.Model):
    """
    Represents inventory records tied to a client.
    Tracks materials, payments, and staff accountability.
    """

    client = models.ForeignKey(
        Client,
        on_delete=models.CASCADE,
        related_name="inventories",
        help_text="The client this inventory record belongs to"
    )

    # Material details
    description = models.TextField(
        verbose_name="Material Description"
    )
    date_of_registration = models.DateField(
        default=timezone.now,
        verbose_name="Date of Registration"
    )
    phone = models.CharField(
        max_length=20,
        blank=True, null=True,
        verbose_name="Phone Number"
    )

    # Financials
    amount_charged = models.DecimalField(max_digits=12, decimal_places=2, verbose_name="Amount Charged")
    amount_deposited = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal("0.00"), verbose_name="Amount Deposited")
    deposit_date = models.DateField(blank=True, null=True, verbose_name="Deposit Date")
    balance = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal("0.00"), verbose_name="Balance")

    # Payment status
    paid_fully = models.BooleanField(default=False, verbose_name="Paid Fully?")
    paid_fully_date = models.DateField(blank=True, null=True, verbose_name="Paid Fully Date")

    # Collection and staff accountability
    collection_date = models.DateField(blank=True, null=True, verbose_name="Collection Date")
    received_by = models.CharField(max_length=150, blank=True, null=True, verbose_name="Received By")
    cleared_by = models.CharField(max_length=150, blank=True, null=True, verbose_name="Cleared By")

    # Automated worker tracking
    created_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        editable=False,  # <--- Crucial: Prevents staff from changing this in forms
        related_name="inventories_created", # Easier to track staff activity
        verbose_name="Created By"
    )

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
        total = self.deposits.aggregate(Sum('amount'))['amount__sum'] or Decimal("0.00")
        self.amount_deposited = total
        
        # Payment Logic
        if self.paid_fully:
            self.balance = Decimal("0.00")
            if not self.paid_fully_date:
                self.paid_fully_date = timezone.now().date()
        else:
            self.balance = max(self.amount_charged - total, Decimal("0.00"))
            if self.balance <= 0:
                self.paid_fully = True
                self.balance = Decimal("0.00")
                if not self.paid_fully_date:
                    self.paid_fully_date = timezone.now().date()
            else:
                self.paid_fully = False
                self.paid_fully_date = None

        self.save(update_fields=["amount_deposited", "balance", "paid_fully", "paid_fully_date"])

class Deposit(models.Model):
    inventory = models.ForeignKey(Inventory, on_delete=models.CASCADE, related_name="deposits")
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    date = models.DateField(default=timezone.now)
    received_by = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.inventory.client} - ₦{self.amount} on {self.date}"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.inventory.update_deposit_summary()

    def delete(self, *args, **kwargs):
        inventory = self.inventory
        super().delete(*args, **kwargs)
        inventory.update_deposit_summary()

auditlog.register(Inventory)
auditlog.register(Deposit)