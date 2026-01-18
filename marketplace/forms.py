from django import forms
from .models import Offering

class OfferingForm(forms.ModelForm):
    class Meta:
        model = Offering
        fields = ['offering_type', 'name', 'hobby', 'description', 'stock_status']