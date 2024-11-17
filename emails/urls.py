from django.urls import path
from . import views
from .views import subscribe, subscribe_thank_you

urlpatterns = [
    # path('signup/', views.email_signup, name='email_signup'),
    path("subscribe/", subscribe, name="subscribe"),
    path(
        "subscribe/thank-you/",
        subscribe_thank_you, name="subscribe_thank_you"
    ),
]
