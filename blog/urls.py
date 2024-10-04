from . import views
from django.urls import path


urlpatterns = [
    path('', views.PostList.as_view(), name='home'),  # List of blog posts
    # Single post detail
    path('<slug:slug>/',
         views.post_detail, name='post_detail'),
]


from . import views
from django.urls import path


urlpatterns = [
    # this is the blog home page that has all the blogs
    # The blog home page/list view
    path("", views.PostList.as_view(), name="home"),
    # Individual Blog posts with slug address
    path('<slug:slug>/', views.post_detail, name='post_detail'), 
]