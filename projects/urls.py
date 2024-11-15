# urls.py
from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.projects, name='projects'),
    path('client-intake/', views.client_intake_view, name='client_intake_form'),
]
