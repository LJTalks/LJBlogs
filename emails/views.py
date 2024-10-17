from django.shortcuts import render, redirect
from .forms import EmailSignupForm
from django.contrib import messages


def email_signup(request):
    next_url = request.GET.get('next', '/')
    
    if request.method == 'POST':
        form = EmailSignupForm(request.POST)
        if form.is_valid():
            subscriber = form.save(commit=False)
            subscriber.source = request.META.get('HTTP_REFERER')
            subscriber.save()
            
            messages.success(request, 'Thank you for subscribing!')
            return redirect(next_url)
    else:
        # Pre-populate the email field if the user is logged in
        if request.user.is_authenticated:
            form = EmailSignupForm(initial={'email': request.user.email})
        else:
            form = EmailSignupForm()
        
    return render(request, 'emails/email_signup.html', {'form': form})
