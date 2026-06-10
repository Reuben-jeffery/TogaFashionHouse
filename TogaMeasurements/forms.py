from django import forms
from .models import MenMeasurement, WomenMeasurement

class MenMeasurementForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Just applying Bootstrap styling, no overriding labels or logic
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})

    class Meta:
        model = MenMeasurement
        exclude = ["client", "date", "updated_at"]

class WomenMeasurementForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})

    class Meta:
        model = WomenMeasurement
        exclude = ["client", "date", "updated_at"]