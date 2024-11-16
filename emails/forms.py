from django import forms
from .models import EmailListSubscriber, ListType


class EmailSignupForm(forms.ModelForm):
    name = forms.CharField(required=False, max_length=100, label="Name")
    # Used for unregistered users or pre-filled for registered users
    email = forms.EmailField(required=True)

    list_type = forms.ModelMultipleChoiceField(
        queryset=ListType.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=True,
        label="Select the types of emails you'd like to receive",
    )

    class Meta:
        model = EmailListSubscriber
        fields = ['email', 'name', 'list_type']

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

        # Pre-fill the email field for authenticated users and disable it
        if user and user.is_authenticated:
            self.fields['email'].initial = user.email
            # Registered users cannot change their email
            self.fields['email'].disabled = True
            self.fields['name'].initial = user.get_full_name()

        # Preselect "regular updates" as default
        regular_update = ListType.objects.filter(
            name="Regular Updates").first()
        if regular_update:
            self.fields['list_type'].initial = [regular_update.id]

        # Populate the list types
        self.fields['list_type'].queryset = ListType.objects.all()
