from django import forms
from captcha.fields import ReCaptchaField
from captcha.widgets import ReCaptchaV2Checkbox


# Recaptcha Global Mixing
class ReCaptchaMixin(forms.Form):
    """A mixin to add reCAPTCHA to forms."""
    captcha = ReCaptchaField(widget=ReCaptchaV2Checkbox())
