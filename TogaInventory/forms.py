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
            # Text fields
            "description": forms.Textarea(attrs={"class": "form-control", "rows": 3}),
            "phone": forms.TextInput(attrs={"class": "form-control"}),

            # Financial fields (numeric inputs, clean placeholders)
            "amount_charged": forms.NumberInput(attrs={
                "class": "form-control",
                "placeholder": "0.00",   # removed ₦ to allow typing
                "step": "0.01"
            }),
            "amount_deposited": forms.NumberInput(attrs={
                "class": "form-control",
                "placeholder": "0.00",
                "step": "0.01"
            }),
            "balance": forms.NumberInput(attrs={
                "class": "form-control",
                "placeholder": "0.00",
                "step": "0.01"
            }),

            # Dates
            "deposit_date": forms.DateInput(attrs={"type": "date", "class": "form-control"}),
            "paid_fully_date": forms.DateInput(attrs={"type": "date", "class": "form-control"}),
            "collection_date": forms.DateInput(attrs={"type": "date", "class": "form-control"}),
            "date_of_registration": forms.DateInput(attrs={"type": "date", "class": "form-control"}),

            # Personnel
            "received_by": forms.TextInput(attrs={"class": "form-control"}),
            "cleared_by": forms.TextInput(attrs={"class": "form-control"}),

            # Status
            "paid_fully": forms.CheckboxInput(attrs={"class": "form-check-input"}),
        }
