from django import forms
from .models import Product


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product

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
            'price': 'price',
            'image_url': 'image_url',
            'image': 'Image',
        }

        self.fields['category'].widget.attrs['autofocus'] = True
        for field in self.fields:
            if field != 'category':
                if self.fields[field].required:
                    placeholder = f'{placeholders[field]} *'
                else:
                    placeholder = placeholders[field]
            self.fields[field].widget.attrs['placeholder'] = placeholder
            self.fields[field].widget.attrs['class'] = 'product-form-input'
            self.fields[field].label = False
