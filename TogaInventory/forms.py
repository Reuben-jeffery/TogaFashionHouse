from django import forms
from .models import Inventory, Deposit
from django.utils import timezone
from decimal import Decimal


class InventoryForm(forms.ModelForm):
    class Meta:
        model = Inventory
        fields = [
            "client",
            "description",
            "phone",
            "amount_charged",
            # removed amount_deposited and balance from user input
            "deposit_date",
            "paid_fully",
            "paid_fully_date",
            "collection_date",
            "received_by",
            "cleared_by",
            "date_of_registration",
        ]
        widgets = {
            "description": forms.Textarea(attrs={"class": "form-control", "rows": 3}),
            "phone": forms.TextInput(attrs={"class": "form-control"}),
            "amount_charged": forms.TextInput(attrs={"class": "form-control currency-input", "placeholder": "0.00"}),
            "deposit_date": forms.DateInput(attrs={"type": "date", "class": "form-control"}),
            "paid_fully_date": forms.DateInput(attrs={"type": "date", "class": "form-control"}),
            "collection_date": forms.DateInput(attrs={"type": "date", "class": "form-control"}),
            "date_of_registration": forms.DateInput(attrs={"type": "date", "class": "form-control"}),
            "received_by": forms.TextInput(attrs={"class": "form-control"}),
            "cleared_by": forms.TextInput(attrs={"class": "form-control"}),
            "paid_fully": forms.CheckboxInput(attrs={"class": "form-check-input"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.data:
            data = self.data.copy()
            # Strip commas and ₦ symbol from amount_charged
            if "amount_charged" in data and data["amount_charged"]:
                data["amount_charged"] = data["amount_charged"].replace(",", "").replace("₦", "")
            self.data = data

    def save(self, commit=True):
        inventory = super().save(commit=False)

        if commit:
            # Save first so it has a primary key
            inventory.save()

            # If Paid Fully is checked, override balance and deposits
            if inventory.paid_fully:
                inventory.amount_deposited = inventory.amount_charged
                inventory.balance = Decimal("0.00")
                if not inventory.paid_fully_date:
                    inventory.paid_fully_date = timezone.now()
                inventory.save()
            else:
                # Ensure balance is recalculated from deposits
                inventory.update_deposit_summary()

        return inventory


class DepositForm(forms.ModelForm):
    class Meta:
        model = Deposit
        fields = ["amount", "date", "received_by"]
        widgets = {
            "amount": forms.TextInput(attrs={"class": "form-control currency-input", "placeholder": "0.00"}),
            "date": forms.DateInput(attrs={"type": "date", "class": "form-control"}),
            "received_by": forms.TextInput(attrs={"class": "form-control"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.data:
            data = self.data.copy()
            # Strip commas and ₦ symbol from deposit amount
            if "amount" in data and data["amount"]:
                data["amount"] = data["amount"].replace(",", "").replace("₦", "")
            self.data = data

    def save(self, commit=True):
        deposit = super().save(commit=False)
        if commit:
            deposit.save()
        return deposit
