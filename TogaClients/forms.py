from django import forms
from .models import Client

class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = ['name', 'phone', 'gender']
        labels = {
            'name': 'Client Name',
            'phone': 'Phone Number',
            'gender': 'Gender Orientation',
        }
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control toga-input-field',
                'placeholder': 'e.g., Chukwuma Bello',
                'autocomplete': 'off',
            }),
            'phone': forms.TextInput(attrs={
                'class': 'form-control toga-input-field',
                'placeholder': 'e.g., 0803 123 4567 or +234...',
                'autocomplete': 'off',
                'inputmode': 'tel',
            }),
            'gender': forms.Select(attrs={
                'class': 'form-select toga-input-field',
            }),
        }

    def clean_phone(self):
        """
        Validates and normalizes Nigerian/International structural phone records.
        """
        phone = self.cleaned_data.get('phone')
        
        if phone:
            # Strip spaces, dashes, and parentheses
            normalized_phone = ''.join(c for c in phone if c.isdigit() or c == '+')
            
            # Basic validation check for digit counts (Nigerian mobile lines typically run 11 digits)
            digits_only = ''.join(c for c in normalized_phone if c.isdigit())
            if len(digits_only) < 7:
                raise forms.ValidationError("Provided sequence is structurally too short for registration.")
                
            return normalized_phone
        return phone