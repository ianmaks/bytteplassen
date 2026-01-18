from django import forms
from .models import Offering, Trade

class OfferingForm(forms.ModelForm):
    class Meta:
        model = Offering
        fields = ['offering_type', 'name', 'hobby', 'description', 'stock_status']

class TradeForm(forms.ModelForm):
    class Meta:
        model = Trade
        fields = ['offered_offering', 'quantity', 'message']
        widgets = {
            'message': forms.Textarea(attrs={'rows': 3}),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user:
            self.fields['offered_offering'].queryset = Offering.objects.filter(owner=user)