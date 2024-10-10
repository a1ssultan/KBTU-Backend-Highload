from django.core.cache import cache
from django.db.models import Prefetch
from django.views import View
from django.views.decorators.cache import cache_page

from .models import Post, Comment, Tag, User

from django.shortcuts import render, get_object_or_404

from .utils import query_debugger


# Create your views here.


# @cache_page(60)
@query_debugger
def all_posts(request):
    # efficient way
    posts = Post.objects.prefetch_related('comments__author').select_related('author').all()

    # not efficient way
    # posts = Post.objects.all()

    return render(request, "blogapp/posts.html", context={"posts": posts})


def get_comment_count(post):
    cache_key = f'comment_count_{post.id}'
    count = cache.get(cache_key)
    if count is None:
        count = post.comments.count()
        cache.set(cache_key, count, timeout=60 * 5)
    return count


@query_debugger
def post_detail(request, pk):
    post = get_object_or_404(
        Post.objects.select_related('author').prefetch_related(
            Prefetch('comments',
                     queryset=Comment.objects.order_by('-created_at')[:10],
                     to_attr='recent_comments')
        ),
        pk=pk
    )
    comment_count = get_comment_count(post)
    recent_comments = post.recent_comments
    return render(request, "blogapp/post_detail.html", context={
        "post": post,
        "comment_count": comment_count,
        "recent_comments": recent_comments
    })


class PostsView(View):
    template_name = "blogapp/posts.html"

    @query_debugger
    def get(self, request):
        post_objects = cache.get('post_objects')

        if post_objects is None:
            post_objects = Post.objects.prefetch_related('comments__author').select_related('author').all()
            cache.set('post_objects', post_objects, timeout=60 * 5)

        context = {
            "posts": post_objects
        }
        return render(request, self.template_name, context)
