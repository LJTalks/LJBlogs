from allauth.account.forms import SignupForm
from django import forms
from ljtalks.models import UserProfile
# from captcha.fields import ReCaptchaField


class ContactForm(forms.Form):
    name = forms.CharField(max_length=100, required=True)
    email = forms.EmailField(required=True)
    message = forms.CharField(widget=forms.Textarea, required=True)
    honeytrap = forms.CharField(required=False, widget=forms.HiddenInput)
    # recaptcha = ReCaptchaField()  # Add reCAPTCHA


class CustomSignupForm(SignupForm):
    def save(self, request):
        user = super(CustomSignupForm, self).save(request)
        
        # Create a UserProfile and save the source and IP
        source = request.META.get('HTTP_REFERER', '')
        ip_address = request.META.get('REMOTE_ADDR', '')
        
        # After saving the user, update the profile or create a profile with
        # the tracking info
        user_profile, created = UserProfile.objects.get_or_create(user=user)
        user_profile.source = source
        user_profile.registration_ip = ip_address
        user_profile.save()
        
        return user