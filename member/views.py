from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.mail import send_mail
from .forms import CustomSignupForm
from .models import UserProfile
from emails.models import EmailListSubscriber
from ljtalks.models import ContactSubmission
from django.conf import settings
import logging
from django.contrib.auth.forms import PasswordChangeForm
# from django.contrib.auth.models import Group
from django.core.exceptions import ValidationError
from django.core.validators import EmailValidator
from allauth.account.views import LoginView
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.views.decorators.cache import never_cache
from django_ratelimit.decorators import ratelimit


def get_user_profile_details(user_id):
    profile = get_object_or_404(UserProfile, user__id=user_id)
    email_subscription = EmailListSubscriber.objects.filter(
        user=profile.user).first()
    contact_submissions = ContactSubmission.objects.filter(
        email=profile.user.email)

    profile_data = {
        "user": profile.user.username,
        "source": profile.source,
        "is_email_subscriber": bool(email_subscription),
        "email_subscription_type": email_subscription.subscribed_list_tyes if email_subscription else None,
        "contact_submissions": [
            submission.message for submission in contact_submissions
        ],
    }

    return profile_data


# Limit to 5 requests per minute per IP
@ratelimit(key='ip', rate='5/m', method='POST', block=True)
def register_user(request):
    # Check if user was rate-limited
    was_limited = getattr(request, 'limits', False)
    if was_limited:
        # Custom response for rate-limited requests
        return HttpResponse(
            "You've made too many requests. Please try again later.",
            status=429
        )

    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            # Create the user
            user = form.save()
            # Capture the source and IP address, inc behind proxies
            ip_address = get_client_ip(request)
            logger.info(f"Captured IP: {ip_address}")

            source = request.META.get('HTTP_REFERER', '')

            # Update the UserProfile with source and IP
            profile, created = UserProfile.objects.get_or_create(user=user)
            profile.source = source
            profile.save()

            return redirect(request.META.get('HTTP_REFERER', 'home'))

    return HttpResponse("Too many requests", status=429)


# IP tracking botwatch
logger = logging.getLogger(__name__)


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0].strip()  # Only the first IP
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


class CustomLoginView(LoginView):
    def form_valid(self, form):
        print("Custom login form_valid triggered")

        login_input = form.cleaned_data.get('login')
        validator = EmailValidator()
        try:
            validator(login_input)
            is_email = True
        except ValidationError:
            is_email = False

        if is_email:
            user_exists = User.objects.filter(email=login_input).exists()
        else:
            user_exists = User.objects.filter(username=login_input).exists()

        if not user_exists:
            messages.error(self.request, "Account not found. Please sign up.")
            return redirect('account_signup')
        return super().form_valid(form)

    def form_invalid(self, form):
        print("Custom login form_invalid triggered")
        # Display error message
        messages.error(
            self.request, "Login failed. Please check your credentials.")
        return super().form_invalid(form)


# Password reset, auto log in
@login_required
def password_reset(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            # Log the user in immediately after password change
            # Prevents logout after password change
            update_session_auth_hash(request, user)
            return redirect('password_change_done')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'account/change_password.html', {'form': form})


# View to handle the "Tester/Beta Access" Form

logger = logging.getLogger(__name__)
# We include is_tester validation but after authentication is checked
# to avoid errors for non logged in users
# renamed from "contact"


@login_required
def beta_contact_view(request):
    is_tester = is_in_group(
        request.user, 'testers')
    return render(request, 'beta_contact.html', {'is_tester': is_tester})


# Apply for beta access form (view)
@login_required
def apply_for_beta_access(request):
    is_tester = is_in_group(request.user, 'testers')

    if request.method == 'POST':
        # Process form submission (email me and store response in db)
        reason = request.POST.get('why')

        # Send an email to notify the admin of the application
        subject = f"{request.user} applied for Beta Access",
        content = (
            f"User {request.user.username} applied for beta access.Reason:\n\n{reason}")

        send_mail(
            subject,
            content,
            settings.DEFAULT_FROM_EMAIL,
            [settings.DEFAULT_FROM_EMAIL]  # Admin email
        )

        # Thank the user and redirect
        messages.success(
            request, 'Thank you for applying for Beta Access. You will be notified when your application is reviewed.')
        return HttpResponseRedirect(reverse('beta_features'))

        # Redirect to beta features page after form submission
        # For now, we'll assume manual approval through the admin panel
        # Redirect after applying
        return HttpResponseRedirect(reverse('beta_features'))

    # Render the beta access form
    return render(request, 'apply_for_beta_access.html', {
        'is_tester': is_tester})


# Helper function to check if the user is in the testers group
def is_in_group(user, group_name):
    # Debugging
    print(f"User: {user}")
    print(f"Groups: {user.groups.all()}")

    # Check if user is in the group
    in_group = user.groups.filter(name=group_name).exists()
    print(f"Is user in group '{group_name}': {in_group}")

    return in_group
    # return user.groups.filter(name=group_name).exists()


# This is the Beta Features View
@login_required
def beta_features_view(request):
    logger.info("Beta Features View Called")

    # Debug Check view is called
    # print("Beta Features View called")
    # Check if user is in the testers group
    is_tester = is_in_group(request.user, 'testers')
    logger.info(f"User {request.user} in in group testers: {is_tester}")
    # Display a list of apps the user has access to
    return render(request, 'beta_features.html', {'is_tester': is_tester})


# Beta Access YouTube Data Checker View
@login_required
@never_cache
def youtube_checker_view(request):
    if not request.user.is_authenticated:
        return redirect('account_login')

    # Check if user is in the testers group
    is_tester = is_in_group(request.user, 'testers')
    if not is_tester:
        # Redirect to safe page if user is not authorised TODO they
        # could get the permission form is they are registered
        # or home page (or back to where they were) if not
        messages.error(request, "You don't have access to this feature.")
        return redirect('home')

    return render(request, 'youtube_checker.html', {'is_tester': is_tester})
