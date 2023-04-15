from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse

from games.models import Game
from posts.models import PostSale, Review
from posts.forms import PostSaleForm, ReviewForm

User = get_user_model()


@login_required
def index(request):
    posts = PostSale.objects.all()
    context = {
        'posts': posts,
    }
    return render(request, 'posts/index.html', context)


@login_required
def post_create(request):
    form = PostSaleForm(
        request.POST or None,
        files=request.FILES or None
    )
    form.fields['game'].queryset = Game.objects.all().filter(
        owner__user=request.user)
    if form.is_valid():
        create_post = form.save(commit=False)
        create_post.author = request.user
        create_post.save()

        return redirect(
            reverse('posts:profile',
                    kwargs={'username': create_post.author.username}))

    context = {
        'form': form
    }

    return render(request, 'posts/create_post.html', context)


@login_required
def post_edit(request, post_id):
    select_post = get_object_or_404(PostSale, id=post_id)
    if request.user != select_post.author:
        return redirect(reverse('posts:index'))
    form = PostSaleForm(
        request.POST or None,
        files=request.FILES or None,
        instance=select_post
    )
    if form.is_valid():
        form.save()
        return redirect(reverse('posts:index'))

    context = {
        'form': form,
        'is_edit': True,
    }

    return render(request, 'posts/create_post.html', context)


@login_required
def post_delete(request, post_id):
    select_post = get_object_or_404(PostSale, id=post_id)
    if request.user != select_post.author:
        return redirect(reverse('posts:index'))
    select_post.delete()
    return redirect(reverse(
        'posts:profile', kwargs={'username': request.user.username}))


@login_required
def profile(request, username):
    author = get_object_or_404(User, username=username)
    user_posts = PostSale.objects.all().filter(
        author__username=username
    )

    context = {
        'author': author,
        'user_posts': user_posts,
    }

    return render(request, 'posts/profile.html', context)


@login_required
def review(request, username):
    author = get_object_or_404(User, username=username)
    reviews = Review.objects.all().filter(user__username=username)
    context = {
        'reviews': reviews,
        'author': author,
    }
    return render(request, 'posts/review.html', context)


@login_required
def review_create(request, username):
    form = ReviewForm(
        request.POST or None,
        files=request.FILES or None
    )
    if form.is_valid():
        create_post = form.save(commit=False)
        create_post.author = request.user
        create_post.user = get_object_or_404(User, username=username)
        create_post.save()

        return redirect(reverse(
            'posts:review', kwargs={'username': create_post.user.username}))

    context = {
        'form': form
    }

    return render(request, 'posts/review_create.html', context)


@login_required
def review_delete(request, username, review_id):
    review = get_object_or_404(Review, id=review_id)
    if review.user == request.user:
        review.delete()
    return redirect('posts:review', username)
