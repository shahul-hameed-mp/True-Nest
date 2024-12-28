from django import forms
from .models import Property

class PropertyForm(forms.ModelForm):
    class Meta:
        model = Property
        fields = [
            'title', 'description', 'price', 'property_type', 'property_for',
            'location', 'beds', 'baths', 'garage', 'sqft', 'built_year',
            'latitude', 'longitude', 'image',
        ]
        widgets = {
            'description': forms.Textarea,
            'latitude': forms.TextInput(attrs={'placeholder': 'Optional'}),
            'longitude': forms.TextInput(attrs={'placeholder': 'Optional'}),
        }
