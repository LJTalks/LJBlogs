from django import forms
from .models import EmailListSubscriber, ListType


class EmailSignupForm(forms.ModelForm):
    email = forms.EmailField(required=True)
   
    class Meta:
        model = EmailListSubscriber
        fields = ['email', 'list_type']

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
       
        # If the user is logged in, aut-fill email field
        if user and user.is_authenticated:
            self.fields['email'].initial = user.email
           
        # Populate the list types
        self.fields['list_type'].queryset = ListType.objects.all()
