from django import forms


class ClientIntakeForm(forms.Form):
    business_name = forms.CharField(max_length=100, label="Business Name")
    business_type = forms.CharField(
        max_length=100, label="Business Type (e.g., retail, service, blog)")
    description = forms.CharField(
        widget=forms.Textarea, label="Briefly describe your business")
    website = forms.URLField(required=False, label="Current Website")
    competitors = forms.CharField(
        widget=forms.Textarea, required=False, label="Main competitors or inspiration sites")
    purpose = forms.MultipleChoiceField(
        choices=[('showcase', 'Showcase Products or Services'),
                 ('sell', 'Sell Products Online'), ...],
        widget=forms.CheckboxSelectMultiple,
        label="Primary Purpose of Website"
    )
    # Add additional fields following this pattern...
