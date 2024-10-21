from django.shortcuts import render, redirect
from .forms import EmailSignupForm
from django.contrib import messages
from django.urls import reverse
from .models import (
    EmailListSubscriber,
    ListType,
    NewsletterEmail,
    SiteContactInfo
)
from django.core.mail import send_mail
import requests
from django.conf import settings


def send_newsletter(list_type_name):
    # Get the list type from the database
    list_type = ListType.objects.get(name=list_type_name)
    # Get the latest newsletter
    newsletter = NewsletterEmail.objects.latest('created_at')
    contact_info = SiteContactInfo.objects.first()
    
    # Prepare email recipients: Subscribers on chosen list type
    recipients = EmailListSubscriber.objects.filter(
        list_type=list_type).values_list('list_email', flat=True)
    # Send the email
    send_mail(
        subject=newsletter.subject,
        message=newsletter.body,
        from_email=contact_info.email,
        recipient_list=list(recipients),
        fail_silently=False,
    )


# views.py
def email_signup(request):
    next_url = request.GET.get('next', '/') or reverse('home')

    if request.method == 'POST':
        
        print(f"Form Data: {request.POST}")
        # Get reCAPTCHA token from the POST data
        recaptcha_response = request.POST.get('g-recaptcha-response')

        # Verify the reCAPTCHA token with Google
        data = {
            'secret': settings.RECAPTCHA_PRIVATE_KEY,  # Your private key
            'response': recaptcha_response
        }
        # Send the request to Google for verification
        r = requests.post(
            'https://www.google.com/recaptcha/api/siteverify', data=data)
        result = r.json()

        # If reCAPTCHA is not successful, return an error
        if not result['success']:
            messages.error(request, 'Invalid reCAPTCHA. Please try again.')
            return redirect('email_signup')
        
        # Form validation and processing continues here...
        form = EmailSignupForm(request.POST, user=request.user)
        print(f"Is form valid? {form.is_valid()}")

        if form.is_valid():
            list_types = form.cleaned_data['list_type']
            source = request.META.get('HTTP_REFERER', '')

            # Fetch the 'Unsubscribed' list type for later use
            unsubscribed_type = ListType.objects.get(name="Unsubscribed")

            # Determine if user is authenticated, set subscriber data
            if request.user.is_authenticated:
                subscriber, created = (
                    EmailListSubscriber.objects.get_or_create(
                        user=request.user,
                        defaults={
                            'list_email': request.user.email, 'source': source
                            }
                        )
                    )
            else:
                email = form.cleaned_data['email']
                subscriber, created = (
                    EmailListSubscriber.objects.get_or_create(
                        list_email=email,
                        defaults={'source': source}
                    )
                )

            # Update list type preferences for auth'd and unauth'd users
            if list_types:
                if unsubscribed_type in list_types and len(list_types) > 1:
                    # Remove 'Unsubscribed' if other lists are selected
                    list_types = [
                        lt for lt in list_types if lt != unsubscribed_type]
                subscriber.list_type.set(list_types)
                messages.success(request, "Your preferences have been updated!")
            else:
                # No lists selected: automatically set 'Unsubscribed'
                subscriber.list_type.clear()
                subscriber.list_type.add(unsubscribed_type)
                messages.info(
                    request, "You've been unsubscribed from all lists.")

            subscriber.save()
            return redirect(next_url)

        else:
            print("Form is not valid.")
            print(form.errors)

    else:
        # Pre-fill the form if authenticated and disable the field
        if request.user.is_authenticated:
            try:
                subscriber = EmailListSubscriber.objects.get(user=request.user)
                form = EmailSignupForm(
                    user=request.user, initial={
                        'list_type': subscriber.list_type.all()})
            except EmailListSubscriber.DoesNotExist:
                form = EmailSignupForm(user=request.user)
        else:
            form = EmailSignupForm()

    return render(request, 'emails/email_signup.html', {'form': form})
