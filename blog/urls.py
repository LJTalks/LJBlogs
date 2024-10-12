from django.urls import path
from . import views


urlpatterns = [
    path('about/', views.about_me, name='about_me'),  # My About Me page URL
    # this is the blog home page that has all the blogs
    # The blog home page/list view
    path('unsubscribe/<int:user_id>/', views.unsubscribe, name='unsubscribe'),
    # Individual Blog posts with slug address
    path('<slug:slug>/', views.post_detail, name='post_detail'),
    path("", views.PostList.as_view(), name="home"),
]
