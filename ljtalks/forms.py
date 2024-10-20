from django import forms
# from captcha.fields import ReCaptchaField


class ContactForm(forms.Form):
    name = forms.CharField(max_length=100, required=True)
    email = forms.EmailField(required=True)
    message = forms.CharField(widget=forms.Textarea, required=True)
    honeytrap = forms.CharField(required=False, widget=forms.HiddenInput)
    # recaptcha = ReCaptchaField()  # Add reCAPTCHA
