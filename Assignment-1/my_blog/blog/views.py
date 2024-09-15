from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseForbidden
from django.template import loader

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from blog.forms import PostForm, CommentForm
from blog.models import Post

# Create your views here.


def home(request):
    return render(request, 'blog/home.html')


def all_posts(request):
    posts = Post.objects.all()
    p = Paginator(posts, 10)
    page_number = request.GET.get('page')
    try:
        page_obj = p.get_page(page_number)
    except PageNotAnInteger:
        page_obj = p.get_page(1)
    except EmptyPage:
        page_obj = p.page(p.num_pages)
    context = {
        'page_obj': page_obj,
    }
    return render(request, 'blog/all_posts.html', context)


def details(request, pk):
    post = Post.objects.get(id=pk)
    comments = post.comments.all()
    form = CommentForm()
    template = loader.get_template('blog/post_detail.html')
    context = {
        'post': post,
        'comments': comments,
        'form': form,
    }
    return render(request, 'blog/post_detail.html', context)


def add_comment(request, pk):
    post = get_object_or_404(Post, id=pk)

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.post = post
            comment.save()
            return redirect('post_details', pk=pk)

    return redirect('post_detail', pk=pk)


def form(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('content')
        author = request.user
        Post.objects.create(title=title, content=content, author=author)
        return redirect('posts')
    else:
        post_form = PostForm()
        return render(request, 'blog/add_post.html', {'form': post_form})


def edit_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.user != post.author:
        return HttpResponseForbidden("You are not allowed to edit this post.")
    if request.method == 'POST':
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            return redirect('posts')
    else:
        form = PostForm(instance=post)

    return render(request, 'blog/edit_post.html', {'form': form, 'post': post})


def delete_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.user != post.author:
        return HttpResponseForbidden("You are not allowed to delete this post.")
    if request.method == 'POST':
        post.delete()
        return redirect('posts')

    return render(request, 'blog/delete_post.html', {'post': post})
