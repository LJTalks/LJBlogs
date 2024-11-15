# views.py
from django.shortcuts import render
from django.http import HttpResponseRedirect
from .forms import ClientIntakeForm
from blog.models import Post
from .models import Project


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


# New client intake form
def client_intake_view(request):
    if request.method == 'POST':
        form = ClientIntakeForm(request.POST)
        if form.is_valid():
            # Process the form data here
            # e.g., save it to the database, send an email, etc.
            return HttpResponseRedirect('/thank-you/')
    else:
        form = ClientIntakeForm()
    return render(request, 'projects/client_intake_form.html', {'form': form})
