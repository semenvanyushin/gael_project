from django.contrib.auth import get_user_model
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404

from gael.settings import PAGINATE_COUNT

User = get_user_model()


class DataMixin:
    paginate_by = PAGINATE_COUNT

    def get_context_data(self, **kwargs):
        '''Добавляет в контекст по ключу "author" пользователя-автора.'''
        context = super().get_context_data(**kwargs)
        context['author'] = get_object_or_404(
            User, username=self.kwargs['username'])
        return context


class ContextAndValidDeleteMixin:
    http_method_names = ['post']

    def form_valid(self, form):
        '''Проверяет соответствие автора запроса автору объекта.'''
        object = self.get_object()
        if object.author != self.request.user:
            return HttpResponseRedirect(self.get_success_url())
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        '''Добавляет в контекст по ключу "author" пользователя-автора.'''
        object = self.get_object()
        context = super().get_context_data(**kwargs)
        context['author'] = object.author
        return context


class AddUserInFormKwargs:

    def get_form_kwargs(self):
        '''Добавляет пользователя в значения формы.'''
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        '''Добавляет пользователя в форму в качестве автора.'''
        form.instance.author = self.request.user
        return super().form_valid(form)
