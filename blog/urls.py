from django.urls import path
from . import views


urlpatterns = [
    # My About Me page URL
    path('about_me/', views.about_me, name='about_me'),
    # this is the blog home page that has all the blogs
    # The blog home page/list view
    # Not sure where this came from
    # It's a view in blogs, move to Profile when it exists
    path('unsubscribe/<int:user_id>/', views.unsubscribe, name='unsubscribe'),
    # Individual Blog posts with slug address
    path("", views.PostList.as_view(), name="home"),
    path("<slug:slug>/", views.post_detail, name="post_detail"),
    path(
        "<slug:slug>/edit_comment/<int:comment_id>",
        views.comment_edit,
        name="comment_edit",
    ),
    path(
        "<slug:slug>/delete_comment/<int:comment_id>",
        views.comment_delete,
        name="comment_delete",
    ),
]