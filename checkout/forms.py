from django import forms
from .models import Order


class OrderForm(forms.ModelForm):
    class Meta:

        model = Order
        fields = ('full_name', 'email', 'phone_number',
                  'street_address', 'town',
                  'postcode', 'request')

    def __init__(self, *args, **kwargs):
        """
        Add placeholders and classes, remove auto-generated
        labels and set autofocus on first field
        """
        super().__init__(*args, **kwargs)
        placeholders = {
            'full_name': 'Full Name',
            'email': 'Email Address',
            'phone_number': 'Phone Number',
            'postcode': 'Post Code',
            'town': 'Town',
            'street_address': 'Street Address',
            'request': 'Please add any special requests you may have'
        }

        self.fields['full_name'].widget.attrs['autofocus'] = True
        for field in self.fields:
            if field != 'town':
                if self.fields[field].required:
                    placeholder = f'{placeholders[field]} *'
                else:
                    placeholder = placeholders[field]
            self.fields[field].widget.attrs['placeholder'] = placeholder
            self.fields[field].widget.attrs['class'] = 'stripe-style-input'
            self.fields[field].label = False
