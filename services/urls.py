from django.urls import path
from . import views

urlpatterns = [
    path('', views.service_list, name='service_list'),  # List of services
    # Detailed view for each service
    path('<int:id>/', views.service_detail, name='service_detail'),
]
