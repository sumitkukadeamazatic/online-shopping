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
        fields = ('name', 'slug', 'description', 'code', 'amount', 'percentage', 'is_for_order', 'minimum',
                  'amount_limit', 'for_new_user', 'valid_from', 'valid_upto', 'start_time', 'end_time', 'days', 'max_count')

    def clean(self):
        cleaned_data = super().clean()
        # Check if 'amount' and 'percentage' values are cleaned or not.
        if set(['amount', 'percentage']).issubset(cleaned_data):
            if cleaned_data['amount'] and cleaned_data['percentage']:
                raise forms.ValidationError(
                    "Set either Amount or Percentage, not both.")
            elif cleaned_data['amount'] is None and cleaned_data['percentage'] is None:
                raise forms.ValidationError(
                    "Set atleast one of amount or percentage.")
        # Restrict admin to put either amount or amount_limit
        if set(['amount', 'amount_limit']).issubset(cleaned_data):
            if cleaned_data['amount'] and cleaned_data['amount_limit']:
                raise forms.ValidationError(
                    "Set either Amount or Amount Limit, not both.")
