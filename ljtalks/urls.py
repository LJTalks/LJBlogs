from django.contrib import admin
from django.urls import path, include
# from django.shortcuts import render
from django.views.generic import TemplateView
from . import views
from member.views import (
    CustomLoginView,
    apply_for_beta_access,
    beta_contact_view,
    beta_features_view
)


# Function to render the maintenance view (if needed)
# def maintenance_view(request):
#     return render(request, 'maintenance.html')

urlpatterns = [
    # Authentication (allauth)
    path('about_me/', views.about_me_view, name='about_me'),
    path('accounts/', include("allauth.urls")),
    path('accounts/login/', CustomLoginView.as_view(), name='account_login'),
    # Admin
    path('admin/', admin.site.urls),
    path('apply_for_beta_access/', apply_for_beta_access,
         name='apply_for_beta_access'),
    path('beta-contact/', beta_contact_view,
         name='beta_contact'),  # Beta Contact URL
    path('beta_features/', beta_features_view, name='beta_features'),
    # path('booking/', include('booking.urls')),
    # General Contact URL (for all)
    path('contact/', views.contact_submit, name='contact'),  # form
    # Include the URLs from the services app
    path('disclaimer/', TemplateView.as_view(
        template_name="ljtalks/disclaimer.html"), name='disclaimer'),
    path('emails/', include('emails.urls')),
    path('member/', include('member.urls')),
    path('notes/', include('notes.urls', namespace='notes')),
    path('privacy/', TemplateView.as_view(
        template_name="ljtalks/privacy.html"), name='privacy_policy'),
    path('products/', include('products.urls')),
    path('projects/', views.projects, name='projects'),
    # path('services/', include('services.urls')),
    path('terms/', TemplateView.as_view(
        template_name="ljtalks/terms.html"), name='terms_conditions'),
    path('youtube/', include('ytapi.urls')),
    # path('info/', views.youtube_info_view, name='youtube-data-checker'),
    path('summernote/', include('django_summernote.urls')),
    path("", include("blog.urls"), name="blog-urls"),
    # path('youtube/', include('ytapi.urls'), name="youtube-data-checker")
]
