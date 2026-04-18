from django import forms
from .models import MenMeasurement, WomenMeasurement

class MenMeasurementForm(forms.ModelForm):
    class Meta:
        model = MenMeasurement
        fields = "__all__"
        exclude = ["client", "date"]

class WomenMeasurementForm(forms.ModelForm):
    class Meta:
        model = WomenMeasurement
        fields = "__all__"
        exclude = ["client", "date"]
