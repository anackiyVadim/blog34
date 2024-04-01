from django.shortcuts import render, get_object_or_404
from django.utils.timezone import now

from .models import Post, Category, Tegs, Subscribe, PostPhoto
from django.db.models import Q
from .forms import PostForm
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


def get_categories():
    all = Category.objects.all()
    count = all.count()
    half = count / 2 + count % 2
    return {'cats1': all[:half], 'cats2': all[half:]}


def index(request):
    posts = Post.objects.all().order_by("-published_date")
    paginator = Paginator(posts, 2)
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
    context = {"posts": posts}
    context.update(get_categories())
    return render(request, 'blog/index.html', context)


def post(request, title=None):
    post = get_object_or_404(Post, title=title)
    imgs = PostPhoto.objects.filter(post=post)
    context = {"post": post, 'imgs': imgs}
    context.update(get_categories())
    return render(request, 'blog/post.html', context)


def about(request):
    context = {}
    context.update(get_categories())
    return render(request, 'blog/about.html', context)


def contact(request):
    context = {}
    context.update(get_categories())
    return render(request, 'blog/contact.html', context)


def category(request, name=None):
    c = get_object_or_404(Category, name=name)
    posts = Post.objects.filter(category=c).order_by("-published_date")
    context = {"posts": posts}
    context.update(get_categories())
    return render(request, 'blog/index.html', context)


def search(request):
    query = request.GET.get('query')
    posts = Post.objects.filter(Q(content__icontains=query) | Q(title__icontains=query))
    context = {"posts": posts}
    context.update(get_categories())
    return render(request, 'blog/index.html', context)


def subscribe(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.save()
            return index(request)


@login_required
def create(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.published_date = now()
            post.user = request.user
            post.save()
            return index(request)
    form = PostForm()
    context = {"form": form}
    context.update(get_categories())
    return render(request, 'blog/create.html', context)

# def logout(request):
#     logout(request)
#     return redirect('index')
