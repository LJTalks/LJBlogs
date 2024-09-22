from django.shortcuts import render, get_object_or_404
from django.views import generic
from .models import Post

# Create your views here.


class PostList(generic.ListView):
    queryset = Post.objects.filter(status=1).order_by("-created_on")
    template_name = "blog/index.html"
    paginate_by = 6


def post_detail(request, slug):
    """
    Display an individual :model:`blog.Post`.
    **Context**
    ``post``
        An instance of :model:`blog.Post`.
    **Template:**

    :template:`blog/post_detail.html`
    """
    

    queryset = Post.objects.filter(status=1)
    # Get the current post
    post = get_object_or_404(queryset, slug=slug)
    # Get the previous post
    previous_post = Post.objects.filter(created_on__lt=post.created_on, status=1).order_by('-created_on').first()
    # Get the next post
    next_post = Post.objects.filter(created_on__gt=post.created_on, status=1).order_by('created_on').first()


    return render(
        request,
        "blog/post_detail.html",
        {
            "post": post,
            "previous_post": previous_post,
            "next_post": next_post,
        },
    )
