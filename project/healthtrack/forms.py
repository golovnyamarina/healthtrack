from django import forms
from .models import Measurement

class MeasurementForm(forms.ModelForm):
    class Meta:
        model = Measurement
        fields = ['upper_pressure', 'lower_pressure', 'pulse', 'note']
        widgets = {
            'upper_pressure': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '120'}),
            'lower_pressure': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '80'}),
            'pulse': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '70'}),
            'note': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),}