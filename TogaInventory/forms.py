from django import forms
from django.utils import timezone
from decimal import Decimal, InvalidOperation
from .models import Inventory, Deposit

class InventoryForm(forms.ModelForm):
    # Overriding to CharField to bypass strict HTML5 number validation
    amount_charged = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control currency-input', 
            'placeholder': '0.00'
        })
    )

    class Meta:
        model = Inventory
        fields = [
            "client", "description", "phone", "amount_charged",
            "deposit_date", "paid_fully", "paid_fully_date",
            "collection_date", "received_by", "cleared_by",
            "date_of_registration",
        ]
        widgets = {
            "description": forms.Textarea(attrs={"rows": 3}),
            "deposit_date": forms.DateInput(attrs={"type": "date"}),
            "paid_fully_date": forms.DateInput(attrs={"type": "date"}),
            "collection_date": forms.DateInput(attrs={"type": "date"}),
            "date_of_registration": forms.DateInput(attrs={"type": "date"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Format existing decimal values as currency strings for the UI
        if self.instance and self.instance.pk and self.instance.amount_charged:
            self.fields['amount_charged'].initial = f"{self.instance.amount_charged:,.2f}"

    def clean_amount_charged(self):
        data = self.cleaned_data.get("amount_charged")
        if data:
            # Strip formatting characters before saving to database
            clean_str = str(data).replace(",", "").replace("₦", "").strip()
            try:
                return Decimal(clean_str)
            except (ValueError, InvalidOperation):
                raise forms.ValidationError("Please provide a valid transaction amount.")
        return data

    def save(self, commit=True):
        inventory = super().save(commit=False)
        if commit:
            inventory.save()
            if inventory.paid_fully:
                inventory.amount_deposited = inventory.amount_charged
                inventory.balance = Decimal("0.00")
                if not inventory.paid_fully_date:
                    inventory.paid_fully_date = timezone.now().date()
                inventory.save()
            else:
                inventory.update_deposit_summary()
        return inventory


class DepositForm(forms.ModelForm):
    amount = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control currency-input'})
    )

    class Meta:
        model = Deposit
        fields = ["amount", "date", "received_by"]
        widgets = {"date": forms.DateInput(attrs={"type": "date"})}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.pk and self.instance.amount:
            self.fields['amount'].initial = f"{self.instance.amount:,.2f}"

    def clean_amount(self):
        data = self.cleaned_data.get("amount")
        if data:
            clean_str = str(data).replace(",", "").replace("₦", "").strip()
            try:
                return Decimal(clean_str)
            except (ValueError, InvalidOperation):
                raise forms.ValidationError("Invalid deposit amount.")
        return data

    def save(self, commit=True):
        deposit = super().save(commit=False)
        if commit:
            deposit.save()
        return deposit