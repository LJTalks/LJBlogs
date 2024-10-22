from django import forms
from allauth.account.adapter import DefaultAccountAdapter
import requests
from django.conf import settings


class CustomAccountAdapter(DefaultAccountAdapter):
    def login(self, request, *args, **kwargs):
        recaptcha_response = request.POST.get('g-recaptcha-response')
        data = {
            'secret': settings.RECAPTCHA_PRIVATE_KEY,
            'response': recaptcha_response
        }
        r = requests.post(
            'https://www.google.com/recaptcha/api/siteverify', data=data)
        result = r.json()
        if not result['success']:
            raise forms.ValidationError("Invalid reCAPTCHA. Please try again.")
        return super().login(request, *args, **kwargs)
