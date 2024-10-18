from django.shortcuts import render, redirect
from .forms import EmailSignupForm
from django.contrib import messages
from .models import EmailListSubscriber


def email_signup(request):
    next_url = request.GET.get('next', '/')

    if request.method == 'POST':
        form = EmailSignupForm(request.POST, user=request.user)  # Pass the user to the form

        if form.is_valid():
            list_types = form.cleaned_data['list_type']
            source = request.META.get('HTTP_REFERER', '')

            # For authenticated users, use their registered email
            if request.user.is_authenticated:
                subscriber, created = EmailListSubscriber.objects.get_or_create(
                    user=request.user,  # Tied to the account
                    defaults={'list_email': request.user.email,
                              'source': source}
                )
                # Update list type preferences
                subscriber.list_type.set(list_types)
                subscriber.save()
            
            # For unauthenticated users, allow them to update preferences if they exist
            else:
                email = form.cleaned_data['email']  # Get email from form
                subscriber, created = EmailListSubscriber.objects.get_or_create(
                    list_email=email,  # Use the provided email for unregistered user
                    defaults={'list_type': list_types, 'source': source}
                )
                # Update list type preferences
                subscriber.list_type.set(list_types)
                subscriber.save()
                
            messages.success(
                request, 'Your preferences have been updated!' if not created else "Thank you for subscribing!")
            return redirect(next_url)

    else:
        # Pre-fill the form if authenticated and disable the field
        if request.user.is_authenticated:
            try:
                subscriber = EmailListSubscriber.objects.get(user=request.user)
                form = EmailSignupForm(
                    user=request.user, initial={'list_type': subscriber.list_type.all()})
            except EmailListSubscriber.DoesNotExist:
                form = EmailSignupForm(user=request.user)
        else:
            form = EmailSignupForm()  # Empty form for unregistered users

    return render(request, 'emails/email_signup.html', {'form': form})
