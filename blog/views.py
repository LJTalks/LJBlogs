from django.shortcuts import (
    render,
    get_object_or_404,
    reverse,
    redirect,
    HttpResponseRedirect
)
from django.views import generic
from django.contrib import messages
from .models import Post, BlogComment, ViewRecord
from .forms import BlogCommentForm
from django.contrib.auth.models import User
import datetime
import os
from django.db.models import Q  # allows for complex queries
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.views.generic import ListView

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


class PostList(generic.ListView):
    model = Post
    template_name = "blog/post_list.html"
    paginate_by = 6

    def get_queryset(self):
        queryset = super().get_queryset().order_by(
            "-publish_date", "-created_on")

        # Include drafts in development
        if os.path.exists('env.py'):
            queryset = queryset.filter(Q(status=1) | Q(status=0))
        else:
            queryset = queryset.filter(status=1)

        query = self.request.GET.get("q")
        if query:
            queryset = queryset.filter(
                Q(title__icontains=query) |
                Q(content__icontains=query) |
                Q(seo_tags__icontains=query)
            )
        return queryset

    def render_to_response(self, context, **response_kwargs):
        if self.request.headers.get('x-requested-with') == 'XMLHttpRequest':
            query = self.request.GET.get("q", "")

            posts = context['object_list']
            posts_html = render_to_string(
                'blog/partials/search_post_list.html', {'posts': posts})
            if posts.exists():
                message = ""
            else:
                message = f'No results found for "{query}"'

            return JsonResponse({'posts_html': posts_html, 'message': message})

        return super().render_to_response(context, **response_kwargs)


def post_detail(request, slug):
    # Include drafts in development
    if os.path.exists('env.py'):
        queryset = Post.objects.filter(Q(status=1) | Q(status=0))
    else:
        queryset = Post.objects.filter(status=1)
    # Get the current post
    post = get_object_or_404(queryset, slug=slug)

    # Track Total no of page views (using sessions to avoid dupes)
    session_key = f"viewed_post_{post.id}"
    if not request.session.get(session_key, False):
        post.views += 1
        post.save()
        request.session[session_key] = True

    # Track views for logged-in users (for recommendations)
    if request.user.is_authenticated:
        # Check ifthe logged in user has already viewed this post
        if not post.viewed_by.filter(id=request.user.id).exists():
            post.viewed_by.add(request.user)

    # Get the previous post
    previous_post = Post.objects.filter(
        publish_date__lt=post.publish_date, status=1).order_by(
            '-publish_date').first()

    # Get the next post
    next_post = Post.objects.filter(
        publish_date__gt=post.publish_date, status=1).order_by(
            'publish_date').first()

    # Get comments
    blog_comments = post.blog_comments.all().order_by("-created_on")
    blog_comment_count = post.blog_comments.filter(status=1).count()

    if request.method == "POST":
        blog_comment_form = BlogCommentForm(data=request.POST)
        if blog_comment_form.is_valid():
            blog_comment = blog_comment_form.save(commit=False)
            blog_comment.author = request.user
            blog_comment.post = post
            blog_comment.save()
            messages.add_message(
                request,
                messages.SUCCESS, "Comment submitted and awaiting approval"
            )
        # Redirect after successful POST to avoid resubmit
        return HttpResponseRedirect(reverse('post_detail', args=[slug]))

    else:
        blog_comment_form = BlogCommentForm()
        # print("about to render template")  # Debug
    return render(
        request,
        "blog/post_detail.html",
        {
            "post": post,
            "previous_post": previous_post,
            "next_post": next_post,
            "blog_comments": blog_comments,
            "blog_comment_count": blog_comment_count,
            "blog_comment_form": blog_comment_form,
        },
    )
    # return render(request, 'blog/post_detail.html', {'post': post})


def blog_comment_edit(request, slug, blog_comment_id):
    """
    view to edit blog_comments
    """

    if request.method == "POST":

        queryset = Post.objects.filter(status=1)
        post = get_object_or_404(queryset, slug=slug)
        blog_comment = get_object_or_404(BlogComment, pk=blog_comment_id)
        blog_comment_form = BlogCommentForm(
            data=request.POST, instance=blog_comment)

        if blog_comment_form.is_valid() and (
            blog_comment.author == request.user
        ):
            blog_comment = blog_comment_form.save(commit=False)
            blog_comment.post = post
            blog_comment.status = 0
            blog_comment.save()
            messages.add_message(request, messages.SUCCESS, 'Comment Updated!')
        else:
            messages.add_message(
                request, messages.ERROR, 'Error updating comment!')

    return HttpResponseRedirect(reverse('post_detail', args=[slug]))


def blog_comment_delete(request, slug, blog_comment_id):
    """
    view to delete comment
    """
    queryset = Post.objects.filter(status=1)
    post = get_object_or_404(queryset, slug=slug)
    blog_comment = get_object_or_404(BlogComment, pk=blog_comment_id)

    if blog_comment.author == request.user:
        blog_comment.delete()
        messages.add_message(request, messages.SUCCESS, 'Comment deleted!')
    else:
        messages.add_message(
            request, messages.ERROR, 'You can only delete your own comments!')

    return HttpResponseRedirect(reverse('post_detail', args=[slug]))
