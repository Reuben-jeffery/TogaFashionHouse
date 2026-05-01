from decimal import Decimal
from django import forms
from .models import Inventory, Deposit


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
            "amount_charged": forms.TextInput(attrs={"class": "form-control currency-input", "placeholder": "0.00"}),
            "amount_deposited": forms.TextInput(attrs={"class": "form-control currency-input", "placeholder": "0.00"}),
            "balance": forms.TextInput(attrs={"class": "form-control currency-input", "placeholder": "0.00"}),
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
        # Strip commas from numeric fields before validation
        if self.data:
            data = self.data.copy()
            for field in ["amount_charged", "amount_deposited", "balance"]:
                if field in data and data[field]:
                    data[field] = data[field].replace(",", "")
            self.data = data


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
        # Strip commas only from the deposit amount field
        if self.data:
            data = self.data.copy()
            if "amount" in data and data["amount"]:
                data["amount"] = data["amount"].replace(",", "")
            self.data = data
