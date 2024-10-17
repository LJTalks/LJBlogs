from django.shortcuts import render, redirect
from .forms import EmailSignupForm
from django.contrib import messages
from .models import ListType, EmailListSubscriber

def email_signup(request):
    next_url = request.GET.get('next', '/')

    if request.method == 'POST':
        form = EmailSignupForm(request.POST, user=request.user)
        if form.is_valid():
            # Check if the user is logged in
            if request.user.is_authenticated:
                # Check if they have already signed up with this email
                subscriber, created = EmailListSubscriber.objects.get_or_create(
                    user=request.user, email=form.cleaned_data['email'], defaults={
                        'list_type': form.cleaned_data['list_type'],
                        'source': request.META.get('HTTP_REFERER'),
                    }
                )
                if not created:
                    subscriber.list_type = form.cleaned_data['list_type']
                    subscriber.save()
            else:
                # If they are not logged in, just save the email and list type
                subscriber, created = EmailListSubscriber.objects.get_or_create(
                    email=form.cleaned_data['email'], defaults={
                        'list_type': form.cleaned_data['list_type'],
                        'source': request.META.get('HTTP_REFERER'),
                    }
                )
                if not created:
                    subscriber.list_type = form.cleaned_data['list_type']
                    subscriber.save()

            messages.success(request, 'Thank you for subscribing!')
            return redirect(next_url)
    else:
        form = EmailSignupForm(user=request.user)

    return render(request, 'emails/email_signup.html', {'form': form})
