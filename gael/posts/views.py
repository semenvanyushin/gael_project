from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from django.views.generic import CreateView, DeleteView, ListView, UpdateView
from django.urls import reverse_lazy

from gael.settings import PAGINATE_COUNT
from posts.models import PostSale, Review
from posts.forms import PostSaleForm, ReviewForm
from posts.utils import (AddUserInFormKwargs, ContextAndValidDeleteMixin,
                         DataMixin)

User = get_user_model()


class MarketPage(ListView):
    '''Выдает список всех постов.'''
    model = PostSale
    paginate_by = PAGINATE_COUNT
    template_name = 'posts/index.html'
    context_object_name = 'posts'
    queryset = PostSale.objects.select_related('author').prefetch_related(
        'account__organizer', 'account__game', 'account__owners')


class PostSaleCreate(LoginRequiredMixin, AddUserInFormKwargs, CreateView):
    '''Создает новый пост.'''
    form_class = PostSaleForm
    template_name = 'posts/create_post.html'


class PostSaleUpdate(LoginRequiredMixin, AddUserInFormKwargs, UpdateView):
    '''Изменяет существующий пост.'''
    model = PostSale
    form_class = PostSaleForm
    template_name = 'posts/create_post.html'
    pk_url_kwarg = 'post_id'


class PostSaleDelete(LoginRequiredMixin, ContextAndValidDeleteMixin,
                     DeleteView):
    '''Удаляет выбранный пост.'''
    model = PostSale
    context_object_name = 'post'
    pk_url_kwarg = 'post_id'
    template_name = 'posts/post_confirm_delete.html'

    def get_success_url(self):
        '''Перенаправляет на страницу пользователя.'''
        return reverse_lazy(
            'posts:profile', kwargs={'username': self.request.user.username})


class ProfilePage(DataMixin, ListView):
    '''Выдает список постов пользователя.'''
    model = PostSale
    template_name = 'posts/profile.html'
    context_object_name = 'user_posts'

    def get_queryset(self):
        '''Выдает все посты пользователя.'''
        return PostSale.objects.filter(
            author__username=self.kwargs['username']).select_related(
                'author').prefetch_related('account__organizer',
                                           'account__game', 'account__owners')


class ReviewPage(DataMixin, ListView):
    '''Выдает список отзывов на пользователя.'''
    model = Review
    template_name = 'posts/review.html'
    context_object_name = 'reviews'

    def get_queryset(self):
        '''Выдает все отзывы на пользователя.'''
        return Review.objects.filter(
            user__username=self.kwargs['username']).select_related(
                'author', 'user')


class ReviewCreate(LoginRequiredMixin, CreateView):
    '''Создает новый отзыв.'''
    form_class = ReviewForm
    template_name = 'posts/review_create.html'

    def form_valid(self, form):
        '''Добавляет в форму автора отзыва и пользователя.'''
        form.instance.author = self.request.user
        form.instance.user = get_object_or_404(
            User, username=self.kwargs['username'])
        return super().form_valid(form)

    def get_success_url(self):
        '''Перенаправляет на страницу с отзывами на пользователя.'''
        return reverse_lazy(
            'posts:review', kwargs={'username': self.kwargs['username']})


class ReviewDelete(LoginRequiredMixin, ContextAndValidDeleteMixin, DeleteView):
    '''Удаляет выбранный отзыв'''
    model = Review
    context_object_name = 'reviews'
    pk_url_kwarg = 'review_id'
    template_name = 'posts/review_confirm_delete.html'

    def get_success_url(self):
        '''Переадресует на страницу с оставшимися отзывами на пользователя.'''
        object = self.get_object()
        return reverse_lazy(
            'posts:review', kwargs={'username': object.user.username})
