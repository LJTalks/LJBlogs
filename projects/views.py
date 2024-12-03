# views.py
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from .forms import ClientIntakeForm
from blog.models import Post
from .models import Project
from .models import ClientIntake


# View to showcase previous projects
def projects(request):
    projects = Project.objects.all().order_by("-created_on")

    latest_post = Post.objects.filter(
        status=1).order_by('-publish_date').first()
    return render(
        request,
        'projects.html',
        {"projects": projects,
         "latest_post": latest_post
         })


# Help page view
def help_page(request):
    return render(request, 'projects/help_page.html')


# New client intake form
@login_required
def client_intake_view(request):
    if request.method == 'POST':
        form = ClientIntakeForm(request.POST)
        if form.is_valid():
            # save form data to client intake model
            # Process the form data here
            # e.g., save it to the database, send an email, etc.
            data = form.cleaned_data
            # Combine multiple purposes into a string
            purposes = ', '.join(data['purpose'])
            ClientIntake.objects.create(
                business_name=data['business_name'],
                business_type=data['business_type'],
                description=data['description'],
                website=data['website'],
                competitors=data['competitors'],
                purpose=purposes
            )
            # Redirect to thank you page
            next_url = request.GET.get('next', reverse('projects'))
            thank_you_url = f'{reverse('thank_you')}?next={next_url}'
            return redirect(thank_you_url)
    else:
        form = ClientIntakeForm()
    return render(request, 'projects/client_intake_form.html', {'form': form})
