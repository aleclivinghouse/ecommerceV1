from django import forms
from django.core.exceptions import ValidationError
from django.core.validators import validate_email

class contactForm(forms.Form):
    name = forms.CharField(required=False, max_length=100, help_text='100 characters max')
    email = forms.EmailField(required=True)
    comment = forms.CharField(widget = forms.Textarea())
    #
    # def clean_name(self):
    #     name = self.cleaned_data.get("name")
    #     if len(name) <= 3:
    #         raise forms.ValidationError("Name must be greater than 3 characters long")
    #     else:
    #         return price
