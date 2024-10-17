from django import forms
from .models import EmailListSubscriber


class EmailSignupForm(forms.ModelForm):
    EMAIL_PREFERENCE_CHOICES = [
        ('weekly', "Weekly Updates"),
        ('news', 'News and Important Changes'),
        ('all', 'I want all the emails!')
    ]

    preferences = forms.MultipleChoiceField(
        choices=EMAIL_PREFERENCE_CHOICES,
        widget=forms.CheckboxSelectMultiple,
        initial=['weekly'],  # Preselect weekly updates
    )

    class Meta:
        model = EmailListSubscriber
        fields = ['email', 'preferences']

