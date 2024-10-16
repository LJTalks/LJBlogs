from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.urls import reverse
# from django.contrib.auth.models import Group
import logging
from django.core.mail import send_mail
from django.conf import settings
from django.contrib import messages


logger = logging.getLogger(__name__)


def contact_submit(request):
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        message = request.POST['message']
        # Prepare the email content
        subject = f"New message from {name}"
        content = f"Message: {message}\n\nFrom: {name}\nEmail: {email}"
        # Send the email
        send_mail(subject, content, email, [settings.DEFAULT_FROM_EMAIL])
        # Show a success message
        messages.success(request, 'Your message has been sent!')

        return redirect('contact')
    

# View to handle the generic contact form
# We include is_tester validation but after authentication is checked 
# to avoid errors for non logged in users
def contact_view(request):
    is_tester = is_in_group(
        request.user, 'testers') if request.user.is_authenticated else False
    return render(request, 'contact.html', {'is_tester': is_tester})


# Apply for special access form (view)
@login_required
def apply_for_special_access(request):
    is_tester = is_in_group(request.user, 'testers')
    if request.method == 'POST':
        # Process form submission (store application ina model,
        # send email, etc)
        # For now, we'll assume manual approval through the admin panel
        # Redirect after applying
        return HttpResponseRedirect(reverse('special_features'))

    # Render the form for applying for access and pass is_tester
    return render(request, 'apply_for_special_access.html', {
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


# This is the Special Features View
@login_required
def special_features_view(request):
    logger.info("Special Features View Called")
    
    # Debug Check view is called
    # print("Special Features View called")
    # Check if user is in the testers group
    is_tester = is_in_group(request.user, 'testers')
    logger.info(f"User {request.user} in in group testers: {is_tester}")
    # Display a list of apps the user has access to
    return render(request, 'special_features.html', {'is_tester': is_tester})


# Special Access YouTube Data Checker View
@login_required
def youtube_checker_view(request):
    # Check if user is in the testers group
    is_tester = is_in_group(request.user, 'testers')
    return render(request, 'youtube_checker.html', {'is_tester': is_tester})
