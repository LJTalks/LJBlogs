from django.urls import path
from . import views

urlpatterns = [
    path('signup/', views.email_signup, name='email_signup'),
]
