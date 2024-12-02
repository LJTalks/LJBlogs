from django import forms
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError


class ClientIntakeForm(forms.Form):
    business_name = forms.CharField(max_length=100, label="Business Name",
                                    widget=forms.TextInput(
                                        attrs={'class': 'form-control'})
                                    )
    business_type = forms.CharField(
        max_length=100, label="Business Type (e.g., retail, service, blog)",
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    description = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'form-control'}),
        label="Briefly describe your business"
    )
    website = forms.CharField(required=False, label="Current Website",
                              widget=forms.TextInput(
                                  attrs={'class': 'form-control'}),
                              help_text="Enter your website URL (e.g., example.com)"
                              )
    competitors = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'form-control'}),
        required=False, label="Main competitors or inspiration sites"
    )
    purpose = forms.MultipleChoiceField(
        choices=[('showcase', 'Showcase Products or Services'),
                 ('sell', 'Sell Products Online'),
                 ('portfolio', 'Portfolio or Resume'),
                 ('community', 'Community Building'),
                 ],
        widget=forms.CheckboxSelectMultiple,
        label="Primary Purpose of Website"
    )
    # Add additional fields following this pattern...
