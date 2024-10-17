from django.contrib import admin
from django.urls import path, include
# from django.shortcuts import render
from . import views
from django.views.generic import TemplateView

# Function to render the maintenance view (if needed)
# def maintenance_view(request):
#     return render(request, 'maintenance.html')

urlpatterns = [
    # Authentication (allauth)
    path('accounts/', include("allauth.urls")),
    # Admin
    path('admin/', admin.site.urls),
    # Restricted to members
    path('apply_for_beta_access/',
         views.apply_for_beta_access,
         name='apply_for_beta_access'),
    # Beta Contact URL (Checks if user is in "testers" group)
    path(
        'beta-contact/', views.beta_contact_view, name='beta_contact'
        ),  # form submit
    # Beta Features (for testers)
    path('beta_features/',
         views.beta_features_view,
         name='beta_features'),
    # path('booking/', include('booking.urls')),
    # General Contact URL (for all)
    path('contact/', views.contact_submit, name='contact'),  # form
    # Include the URLs from the services app
    path('disclaimer/', TemplateView.as_view(
        template_name="ljtalks/disclaimer.html"), name='disclaimer'),
    path('emails/', include('emails.urls')),
    path('privacy/', TemplateView.as_view(
        template_name="ljtalks/privacy.html"), name='privacy_policy'),
    # path('services/', include('services.urls')),
    path('terms/', TemplateView.as_view(
        template_name="ljtalks/terms.html"), name='terms_conditions'),
    path('youtube/', include('ytapi.urls')),
    # path('info/', views.youtube_info_view, name='youtube-data-checker'),
    path('summernote/', include('django_summernote.urls')),
    path("", include("blog.urls"), name="blog-urls"),
    # Think we replaced this with the restricted tester only api path above
    # Public or other features (different to the api path, not sure how!)
    # path('youtube/', include('ytapi.urls'), name="youtube-data-checker")
]
