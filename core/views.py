from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods



# Create your views here.

from django.views import generic
from .models import Post

class Index(generic.ListView):
    """
    Generic class-based view for a list of all posts.
    """
    model = Post
    paginate_by = 5

class PostDetailView(generic.DetailView):
    """
    Generic detail view for a post
    """
    model = Post

class AuthorDetailView(generic.DetailView):
    """
    Generic detail view for an author
    """
    model = User


@require_http_methods(['POST'])
@login_required
def post_favorite_view(request, post_pk):
    post = get_object_or_404(Post, pk=post_pk)

    # We want to toggle whether this post is favorited.
    # If we find a favorite with this user and post (i.e. it is not created
    # prior to this moment) then delete that favorite, otherwise create it.
    
    if post in request.user.favorite_posts.all():
        request.user.favorite_posts.remove(post)
    else:
        request.user.favorite_posts.add(post)

    return redirect(request.META.get('HTTP_REFERER', '/'))