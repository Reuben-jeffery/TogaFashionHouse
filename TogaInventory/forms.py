from django import forms
from .models import Inventory


class InventoryForm(forms.ModelForm):
    class Meta:
        model = Inventory
        fields = [
            "client",
            "description",
            "phone",
            "amount_charged",
            "amount_deposited",
            "deposit_date",
            "balance",
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
            "amount_charged": forms.NumberInput(attrs={"class": "form-control"}),
            "amount_deposited": forms.NumberInput(attrs={"class": "form-control"}),
            "deposit_date": forms.DateInput(attrs={"type": "date", "class": "form-control"}),
            "balance": forms.NumberInput(attrs={"class": "form-control"}),
            "paid_fully": forms.CheckboxInput(attrs={"class": "form-check-input"}),
            "paid_fully_date": forms.DateInput(attrs={"type": "date", "class": "form-control"}),
            "collection_date": forms.DateInput(attrs={"type": "date", "class": "form-control"}),
            "received_by": forms.TextInput(attrs={"class": "form-control"}),
            "cleared_by": forms.TextInput(attrs={"class": "form-control"}),
            "date_of_registration": forms.DateInput(attrs={"type": "date", "class": "form-control"}),
        }
