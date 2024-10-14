from django.shortcuts import render
from django.contrib.auth.decorators import login_required


# View to handle the contact form
def contact_view(request):
    return render(request, 'contact.html')


# Helper function to check if the user is in  the testers group
def is_in_group(user, group_name):
    return user.groups.filter(name=group_name).exists()


# This is the Special Features View
def special_features_view(request):
    # Check if user is in the testers group
    is_tester = is_in_group(request.user, 'testers')
    # Display a list of apps the user has access to
    return render(request, 'special_features_html', {'is_tester': is_tester})


# YouTube Data Checker View
@login_required
def youtube_checker_view(request):
    # Check if user is in the testers group
    is_tester = is_in_group(request.user, 'testers')
    return render(request, 'youtube_checker.html', {'is_tester': is_tester})


def apply_for_special_access(request):
    return render(request, 'apply_for_special_access.html')
