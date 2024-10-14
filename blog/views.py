from django.shortcuts import render, get_object_or_404, reverse, redirect
from django.views import generic
from django.contrib import messages
from .models import Post, Comment
from django.http import HttpResponseRedirect
from .forms import CommentForm
from django.contrib.auth.models import User
from .forms import CommentForm  # crispy


# Unsubscribe view, maybe not the best app for it?
def unsubscribe(request, user_id):
    try:
        user = User.objects.get(pk=user_id)
        # Logic to remove user from email lists or mark them as unsubscribed
        user.profile.is_subscribed = False
        user.profile.save()
        messages.success(request, 'You have been unsubscribed successfully.')
    except User.DoesNotExist:
        messages.error(request, 'User not found.')
    return redirect('homepage')


def about_me(request):
    return render(request, 'blog/about_me.html')  # My About Me page


class PostList(generic.ListView):
    queryset = Post.objects.filter(status=1).order_by("-created_on")
    template_name = "blog/post_list.html"
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
    previous_post = Post.objects.filter(
        created_on__lt=post.created_on, status=1).order_by(
            '-created_on').first()
    # Get the next post
    next_post = Post.objects.filter(
        created_on__gt=post.created_on, status=1).order_by(
            'created_on').first()

    # Comments
    comments = post.comments.all().order_by("-created_on")
    comment_count = post.comments.filter(approved=True).count()

    if request.method == "POST":
        print("received a POST request")
        comment_form = CommentForm(data=request.POST)

        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.author = request.user
            comment.post = post
            comment.save()
            messages.add_message(
                request,
                messages.SUCCESS, "Comment submitted and awaiting approval"
            )

    comment_form = CommentForm()
    # print("about to render template")  # Debug

    return render(
        request,
        "blog/post_detail.html",
        {
            "post": post,
            "previous_post": previous_post,
            "next_post": next_post,
            "comments": comments,
            "comment_count": comment_count,
            "comment_form": comment_form,
        },
    )

def comment_edit(request, slug, comment_id):
    """
    view to edit comments
    """
   
    if request.method == "POST":
       
        queryset = Post.objects.filter(status=1)
        post = get_object_or_404(queryset, slug=slug)
        comment = get_object_or_404(Comment, pk=comment_id)
        comment_form = CommentForm(data=request.POST, instance=comment)
       
        if comment_form.is_valid() and comment.author == request.user:
            comment = comment_form.save(commit=False)
            comment.post = post
            comment.approved = False
            comment.save()
            messages.add_message(request, messages.SUCCESS, 'Comment Updated!')
        else:
            messages.add_message(
                request, messages.ERROR, 'Error updating comment!')
            
    return HttpResponseRedirect(reverse('post_detail', args=[slug]))


def comment_delete(request, slug, comment_id):
    """
    view to delete comment
    """
    queryset = Post.objects.filter(status=1)
    post = get_object_or_404(queryset, slug=slug)
    comment = get_object_or_404(Comment, pk=comment_id)
    
    if comment.author == request.user:
        comment.delete()
        messages.add_message(request, messages.SUCCESS, 'Comment deleted!')
    else:
        messages.add_message(
            request, messages.ERROR, 'You can only delete your own comments!')
        
    return HttpResponseRedirect(reverse('post_detail', args=[slug]))
                 