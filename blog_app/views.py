from django.shortcuts import render
from django.db.models import Q
from django.contrib.auth.decorators import login_required

from django.http import JsonResponse
from .models import Post, Like

from django.contrib import messages

from django.contrib.auth.models import User

# Create your views here.
from .models import Post
from django.shortcuts import render, get_object_or_404,redirect
from .forms import PostForm,RegisterForm
from .models import Category,Post
from .forms import CommentForm


from django.contrib.auth.decorators import login_required

from django.core.paginator import Paginator

from django.contrib.auth.decorators import login_required


@login_required
def home(request):

    query = request.GET.get("q")

    if query:
        posts = Post.objects.filter(
            Q(title__icontains=query) |
            Q(content__icontains=query)
        ).order_by("-created_at")

    else:
        posts = Post.objects.all().order_by("-created_at")


    paginator = Paginator(posts, 5)   # Show 5 posts per page

    page_number = request.GET.get("page")

    page_obj = paginator.get_page(page_number)


    return render(request, "blog_app/home.html", {
        "page_obj": page_obj,
        "query": query,
    })


def post_detail(request, id):
    post = get_object_or_404(Post, id=id)

    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.user = request.user
            comment.save()
            return redirect("post_detail", id=post.id)
    else:
        form = CommentForm()

    return render(
        request,
        "blog_app/post_detail.html",
        {
            "post": post,
            "form": form,
        },
    )

@login_required
def create_post(request):
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('home')
    else:
        form = PostForm()

    return render(request, 'blog_app/create_post.html', {'form': form})

@login_required
def update_post(request, id):
    post = get_object_or_404(Post, id=id)

    # Only the author can edit
    if post.author != request.user:
        return redirect('home')

    if request.method == "POST":
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
            return redirect('post_detail', id=post.id)
    else:
        form = PostForm(instance=post)

    return render(request, "blog_app/update_post.html", {"form": form})

@login_required
def delete_post(request, id):
    post = get_object_or_404(Post, id=id)

    # Only the author can delete
    if post.author == request.user:
        post.delete()

    return redirect('home')

def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("login")
    else:
        form = RegisterForm()

    return render(request, "blog_app/register.html", {"form": form})

def category_posts(request, id):
    category = Category.objects.get(id=id)
    posts = Post.objects.filter(category=category)

    return render(
        request,
        "blog_app/home.html",
        {"posts": posts}
    )
    
    
@login_required
def like_post(request, id):

    post = get_object_or_404(Post, id=id)

    if request.user in post.likes.all():

        # Unlike
        post.likes.remove(request.user)

    else:

        # Like
        post.likes.add(request.user)

    return redirect("home")

@login_required
def profile(request, id):

    profile_user = get_object_or_404(User, id=id)

    posts = Post.objects.filter(
        author=profile_user
    )

    # Show email only to profile owner
    show_email = request.user == profile_user


    context = {

        "profile_user": profile_user,
        "posts": posts,
        "show_email": show_email

    }


    return render(
        request,
        "blog_app/profile.html",
        context
    )

def register(request):

    if request.method == "POST":

        form = RegisterForm(request.POST)

        if form.is_valid():
            form.save()

            messages.success(request, "Account created successfully.")

            return redirect("login")

    else:

        form = RegisterForm()

    return render(request, "blog_app/register.html", {"form": form})

