"""
Offer App Forms
"""

from django import forms
from .models import Offer


class OfferForm(forms.ModelForm):
    """
    Using this Form for offer in django admin
    """

    class Meta:
        model = Offer
        exclude = ('created_at', 'updated_at')

    def clean(self):
        cleaned_data = super().clean()
        form_data_keys = cleaned_data.keys()
        # Check if 'amount' and 'percentage' values are cleaned or not.
        if set(['amount', 'percentage']).issubset(cleaned_data):
            if cleaned_data['amount'] and cleaned_data['percentage']:
                raise forms.ValidationError(
                    "Set either Amount or Percentage, not both.")
            elif cleaned_data['amount'] is None and cleaned_data['percentage'] is None:
                raise forms.ValidationError(
                    "Set atleast one of amount or percentage.")
