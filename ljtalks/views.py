from django.shortcuts import render, redirect
from datetime import date
from blog.models import Post
from .forms import ContactForm
from django.contrib import messages
from django.conf import settings
from django.core.mail import EmailMessage
import requests
from ljtalks.models import ContactSubmission


# How Many Days I've been Coding count
def about_me_view(request):
    start_date = date(2024, 6, 24)
    current_date = date.today()
    days_coding = (current_date - start_date).days

    latest_post = Post.objects.filter(status=1).latest(
        'publish_date')

    return render(request, 'about_me.html', {
        'days_coding': days_coding,
        'latest_post': latest_post
    })


# View to showcase previous projects
def projects(request):
    projects = [
        {
            "title": "Heartland Hub",
            "description": "A community-driven platform designed to connect users with local, home-based, and traditional businesses. It offers a directory of authentic, craft-focused enterprises, enabling artisans and small business owners to showcase their work and reach a broader audience.",
            "link": "https://heartlandhub.co.uk/",
            "image": "images/projects_heartland.png",
        },
        {
            "title": "Berkshire Printmakers",
            "description": "Berkshire Printmakers deliver bespoke silk screen printing workshops to inspire creativity and connection. The workshops offer engaging, hands-on experiences for all ages. Combining traditional techniques with modern applications. Perfect for team-building events, creative retreats, or unique experiences, bringing art and collaboration to life.",
            "link": "https://berkshireprintmakers.com/",
            "image": "images/project_images/berkshireprintmakers.png",
        },
        {
            "title": "The Fallen; A Simple (free) Landing Page",
            "description": "Simple one page landing page to promote a young author's new book.",
            "link": "https://ltjones.carrd.co/",
            "image": "images/projects_thefallen.png",
        },
        {
            "title": "Love Running",
            "description": "A Fictional Running/Social club advertising regular meets. Responsive HTML & CSS. A Code Institute Tutorial, for a social/running club. Hosted on GitHub Pages.",
            "link": "https://ljtalks.github.io/love-running/",
            "image": "images/projects_love-running.png",
        },
        {
            "title": "Whiskey Store",
            "description": "A Fictional Online Whiskey Subscription site. Responsive HTML, CSS and JavaScript. A Code Institute tutorial. Hosted on Github Pages.",
            "link": "https://ljtalks.github.io/whiskey-store/",
            "image": "images/projects_whiskey-drop.png",
        },
        {
            "title": "Love Rosie; A Resume/CV site",
            "description": "A Fictional Online Resume/CV. Responsive HTML, CSS, JavaScript, Bootstrap 4. A Code Institute tutorial. Hosted on Github Pages.",
            "link": "https://ljtalks.github.io/UCD-Resume/",
            "image": "images/projects_love-rosie.png",
        },
        {
            "title": "Inspire Me Journal; My first JavaScript Project",
            "description": "JavaScript web application. Responsive HTML, CSS, JavaScript. Personal project. Hosted on Github pages.",
            "link": "https://ljtalks.github.io/my-new-journal/",
            "image": "images/inspire_me_journal.png",
        },
        {
            "title": "Codestar Blog; A Full Stack Web App",
            "description":
                "Full stack web application using Django, PostgreSQL, Python, Responsive HTML, CSS, JavaScript, Bootstrap 4. A Code Institute tutorial. Hosted on Heroku.",
            "link": "https://ljtalks-django-blog-5fbe7cf2584e.herokuapp.com/",
            "image": "images/projects_love-rosie.png",
        },
    ]

    latest_post = Post.objects.filter(status=1).latest('publish_date')
    return render(
        request,
        'projects.html',
        {"projects": projects,
            "latest_post": latest_post
         })


# General contact form (for anyone)
def contact_submit(request):
    if request.method == 'POST':
        # Get reCAPTCHA token from the POST data
        recaptcha_response = request.POST.get('g-recaptcha-response')

        # Verify the reCAPTCHA token with Google
        data = {
            'secret': settings.RECAPTCHA_PRIVATE_KEY,
            'response': recaptcha_response
        }
        # Send the request to Google for verification
        r = requests.post(
            'https://www.google.com/recaptcha/api/siteverify', data=data)
        result = r.json()

        # If reCAPTCHA is not successful, return an error
        if not result['success']:
            messages.error(request, 'Invalid reCAPTCHA. Please try again.')
            return redirect('contact')

        form = ContactForm(request.POST)

        if form.is_valid():
            # Check the honeypot field
            if form.cleaned_data['honeytrap']:
                # If field is completed it's bot's
                # Redirect without sending any email or showing any message
                return redirect('contact')
            else:
                # Process the valid form submission from a real user
                name = form.cleaned_data['name']
                email = (
                    request.user.email
                    if request.user.is_authenticated
                    else form.cleaned_data['email'])
                message = form.cleaned_data['message']

                # Save to database
                ContactSubmission.objects.create(
                    user=request.user if request.user.is_authenticated else None,
                    name=name,
                    email=email,
                    message=message
                )

                # Prepare and send the email
                subject = f"LJTalks Contact Form from {name}"
                content = (
                    f"New Message from: {name}\nEmail: {email}\n\n{message}\n")
                # Send the email
                email_message = EmailMessage(
                    subject=subject,
                    body=content,
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    to=[settings.DEFAULT_FROM_EMAIL],
                    reply_to=[email]
                )
                # Set X_Priority to flag the email as important
                email_message.extra_headers = {'X-Priority': '1'}
                email_message.send()

                # Show a success message
                messages.success(request, 'Your message has been sent!')

                # Get the next parameter from form and redirect back
                next_url = request.POST.get('next') or 'home'
                return redirect(next_url)
        else:
            messages.error(request, 'There was an error in the form.')
    else:
        initial_data = {
            'email': request.user.email} if request.user.is_authenticated else {}
        # If GET request, just render the empty form
        form = ContactForm(initial=initial_data)

    # For a GET request, just render the contact form
    return render(request, 'contact.html', {'form': form})
