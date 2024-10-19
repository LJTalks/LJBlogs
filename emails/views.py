from django.shortcuts import render, redirect
from .forms import EmailSignupForm
from django.contrib import messages
from django.urls import reverse
from .models import EmailListSubscriber, ListType  # Include ListType model


# views.py
def email_signup(request):
    next_url = request.GET.get('next', '/') or reverse('home')

    if request.method == 'POST':
        print(f"Form Data: {request.POST}")

        form = EmailSignupForm(request.POST, user=request.user)

        print(f"Is form valid? {form.is_valid()}")

        if form.is_valid():
            list_types = form.cleaned_data['list_type']
            source = request.META.get('HTTP_REFERER', '')

            # Fetch the 'Unsubscribed' list type for later use
            unsubscribed_type = ListType.objects.get(name="Unsubscribed")

            # For authenticated users, use their registered email
            if request.user.is_authenticated:
                subscriber, created = EmailListSubscriber.objects.get_or_create(
                    user=request.user,
                    defaults={'list_email': request.user.email, 'source': source}
                )
                # Update list type preferences
                if list_types:
                    if unsubscribed_type in list_types and len(list_types) > 1:
                        # Remove 'Unsubscribed' if other lists are selected
                        list_types = [lt for lt in list_types if lt != unsubscribed_type]
                    subscriber.list_type.set(list_types)
                    messages.success(request, "Your preferences have been updated!")
                else:
                    # No lists selected: automatically set 'Unsubscribed'
                    subscriber.list_type.set([unsubscribed_type])
                    messages.info(request, "You've been unsubscribed from all lists.")

                subscriber.save()

            # For unauthenticated users
            else:
                email = form.cleaned_data['email']
                subscriber, created = EmailListSubscriber.objects.get_or_create(
                    list_email=email,
                    defaults={'list_type': list_types, 'source': source}
                )
                # Update list type preferences
                if list_types:
                    if unsubscribed_type in list_types and len(list_types) > 1:
                        # Remove 'Unsubscribed' if other lists are selected
                        list_types = [lt for lt in list_types if lt != unsubscribed_type]
                    subscriber.list_type.set(list_types)
                    messages.success(request, "Your preferences have been updated!")
                else:
                    # No lists selected: automatically set 'Unsubscribed'
                    subscriber.list_type.clear()
                    messages.info(request, "We're sorry to see you go. You've been unsubscribed from all lists.")

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
                    user=request.user, initial={'list_type': subscriber.list_type.all()})
            except EmailListSubscriber.DoesNotExist:
                form = EmailSignupForm(user=request.user)
        else:
            form = EmailSignupForm()

    return render(request, 'emails/email_signup.html', {'form': form})
