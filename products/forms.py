from django import forms
from .models import Product


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        """
        Add placeholders and classes, remove auto-generated
        labels and set autofocus on first field
        """
        super().__init__(*args, **kwargs)
        placeholders = {
            'category': 'Category',
            'name': 'Name',
            'description': 'Description',
            'spice_index': 'Spice Index',
            'availability': 'Availability',
            'price': 'price',
            'image_url': 'image_url',
            'image': 'Image',
        }

        self.fields['category'].widget.attrs['autofocus'] = True
        for field in self.fields:
            if field != 'category' and field != 'spice_index':
                if self.fields[field].required:
                    self.fields[field].widget.attrs[
                        'placeholder'] = f'{placeholders[field]} *'
                else:
                    self.fields[field].widget.attrs[
                        'placeholder'] = placeholders[field]
            self.fields[field].widget.attrs[
                'class'] = 'border-black rounded-0 product-form-input'
            if field != 'availability':
                self.fields[field].label = False
            else:
                self.fields[field].label = "Item Available"
                