from django.urls import path
from . import views

urlpatterns = [
    path('', views.PostList.as_view(), name='home'),  # List of blog posts
    path('<slug:slug>/', views.post_detail, name='post_detail'),  # Single post detail
]
