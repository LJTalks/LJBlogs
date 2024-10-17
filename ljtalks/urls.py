from django.contrib import admin
from django.urls import path, include
# from django.shortcuts import render
from . import views
from django.views.generic import TemplateView

# Function to render the maintenance view (if needed)
# def maintenance_view(request):
#     return render(request, 'maintenance.html')

urlpatterns = [
    path('accounts/', include("allauth.urls")),
    path('admin/', admin.site.urls),
    # Restricted to testers
    path('apply_for_beta_access/',
         views.apply_for_beta_access,
         name='apply_for_beta_access'),
    # General Contact URL (for anyone)
    path('contact/', views.contact_submit, name='contact'),  # form
    # Beta Contact URL (Checks if user is in "testers" group)
    path(
        'beta-contact/', views.beta_contact_view, name='beta_contact'
        ),  # form submit
    # Apply for Beta Access (logged in users only)
    path('apply-for-beta-access/', views.apply_for_beta_access, name='apply_for_beta_access'),
    # Beta Features (for testers)
    path('beta-features/', views.beta_features_view, name='beta_features'),
    # path('info/', views.youtube_info_view, name='youtube-data-checker'),
    # path('booking/', include('booking.urls')),
    # Include the URLs from the services app
    # path('services/', include('services.urls')),
    path('youtube/', include('ytapi.urls')),
    path('beta_features/',
         views.beta_features_view,
         name='beta_features'),
    path('privacy/', TemplateView.as_view(
        template_name="ljtalks/privacy.html"), name='privacy_policy'),
    path('terms/', TemplateView.as_view(
        template_name="ljtalks/terms.html"), name='terms_conditions'),
    path('disclaimer/', TemplateView.as_view(
        template_name="ljtalks/disclaimer.html"), name='disclaimer'),
    path('summernote/', include('django_summernote.urls')),
    path("", include("blog.urls"), name="blog-urls"),
    # Think we replaced this with the restricted tester only api path above
    # Public or other features (different to the api path, not sure how!)
    # path('youtube/', include('ytapi.urls'), name="youtube-data-checker")
]
