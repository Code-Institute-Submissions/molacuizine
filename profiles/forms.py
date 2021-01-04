from django import forms
from .models import UserProfile


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        # Field already created at sign-up
        exclude = ('user',)

    def __init__(self, *args, **kwargs):
        """
        Add placeholders and classes, remove auto-generated
        labels and set autofocus on first field
        """
        super().__init__(*args, **kwargs)
        placeholders = {
            'default_phone_number': 'Phone Number',
            'default_street_address1': 'Street Address 1',
            'town': 'Street Address 2',
            'default_postcode': 'County, State or Locality',
        }

        self.fields['default_phone_number'].widget.attrs['autofocus'] = True
        for field in self.fields:
            self.fields[field].widget.attrs[
                'placeholder'] = placeholders[field]
            self.fields[field].widget.attrs[
                'class'] = 'border-black rounded-0 profile-form-input'
            self.fields[field].label = False
