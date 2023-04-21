from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Prefetch
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.views.generic import CreateView, DeleteView, ListView, UpdateView
from django.urls import reverse_lazy

from games.models import Owner
from posts.models import PostSale, Review
from posts.forms import PostSaleForm, ReviewForm
from posts.utils import DataMixin

User = get_user_model()


class MarketPage(DataMixin, ListView):
    '''Выдает список всех постов.'''
    model = PostSale
    template_name = 'posts/index.html'
    context_object_name = 'posts'
    queryset = PostSale.objects.select_related(
        'author', 'game').prefetch_related(Prefetch(
            'game__owner', queryset=Owner.objects.select_related(
                'account', 'user').prefetch_related('account__organizer')))


class PostSaleCreate(LoginRequiredMixin, CreateView):
    '''Создает новый пост.'''
    form_class = PostSaleForm
    template_name = 'posts/create_post.html'

    def get_form_kwargs(self):
        kwargs = super(PostSaleCreate, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super(PostSaleCreate, self).form_valid(form)


class PostSaleUpdate(LoginRequiredMixin, UpdateView):
    '''Изменяет существующий пост.'''
    model = PostSale
    form_class = PostSaleForm
    template_name = 'posts/create_post.html'
    pk_url_kwarg = 'post_id'

    def get_form_kwargs(self):
        kwargs = super(PostSaleUpdate, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs


class PostSaleDelete(LoginRequiredMixin, DeleteView):
    '''Удаляет выбранный пост.'''
    model = PostSale
    http_method_names = ['post']
    context_object_name = 'post'
    pk_url_kwarg = 'post_id'
    template_name = 'posts/post_confirm_delete.html'

    def get_success_url(self):
        return reverse_lazy(
            'posts:profile', kwargs={'username': self.request.user.username})

    def get_context_data(self, **kwargs):
        object = self.get_object()
        context = super().get_context_data(**kwargs)
        context['author'] = object.author
        return context

    def form_valid(self, form):
        object = self.get_object()
        if object.author != self.request.user:
            return HttpResponseRedirect(self.get_success_url())
        return super(PostSaleDelete, self).form_valid(form)


class ProfilePage(LoginRequiredMixin, DataMixin, ListView):
    '''Выдает список постов пользователя.'''
    model = PostSale
    template_name = 'posts/profile.html'
    context_object_name = 'user_posts'

    def get_queryset(self):
        return PostSale.objects.filter(
            author__username=self.kwargs['username']).select_related(
                'author', 'game').prefetch_related(Prefetch(
                    'game__owner', queryset=Owner.objects.select_related(
                        'account', 'user').prefetch_related(
                            'account__organizer')))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['author'] = get_object_or_404(
            User, username=self.kwargs['username'])
        return context


class ReviewPage(LoginRequiredMixin, DataMixin, ListView):
    '''Выдает список отзывов на пользователя.'''
    model = Review
    template_name = 'posts/review.html'
    context_object_name = 'reviews'

    def get_queryset(self):
        return Review.objects.filter(
            user__username=self.kwargs['username']).select_related(
                'author', 'user')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['author'] = get_object_or_404(
            User, username=self.kwargs['username'])
        return context


class ReviewCreate(LoginRequiredMixin, CreateView):
    '''Создает новый отзыв.'''
    form_class = ReviewForm
    template_name = 'posts/review_create.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.user = get_object_or_404(
            User, username=self.kwargs['username'])
        return super(ReviewCreate, self).form_valid(form)

    def get_success_url(self):
        return reverse_lazy(
            'posts:review', kwargs={'username': self.kwargs['username']})


class ReviewDelete(LoginRequiredMixin, DeleteView):
    '''Удаляет выбранный отзыв'''
    model = Review
    http_method_names = ['post']
    context_object_name = 'reviews'
    pk_url_kwarg = 'review_id'
    template_name = 'posts/review_confirm_delete.html'

    def get_success_url(self):
        object = self.get_object()
        return reverse_lazy(
            'posts:review', kwargs={'username': object.user.username})

    def get_context_data(self, **kwargs):
        object = self.get_object()
        context = super().get_context_data(**kwargs)
        context['author'] = object.user
        return context

    def form_valid(self, form):
        object = self.get_object()
        if object.author != self.request.user:
            return HttpResponseRedirect(self.get_success_url())
        return super(ReviewDelete, self).form_valid(form)
