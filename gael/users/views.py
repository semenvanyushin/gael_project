from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, UpdateView

from users.forms import CreationForm, AdditionsToTheProfileForm
from users.models import AdditionsToTheProfile
from users.utils import DataMixin

User = get_user_model()


class SignUp(CreateView):
    form_class = CreationForm
    success_url = reverse_lazy('users:login')
    template_name = 'users/signup.html'


class AdditionsToTheProfile(LoginRequiredMixin, ListView):
    '''Выдает данные профиля.'''
    model = AdditionsToTheProfile
    template_name = 'users/user_profile.html'
    context_object_name = 'profile'
    pk_url_kwarg = 'username'

    def get_queryset(self):
        '''Выдает данные пользователя пользователя.'''
        return AdditionsToTheProfile.objects.filter(user=self.response.user)


class AdditionsToTheProfileCreate(LoginRequiredMixin, CreateView):
    '''Создает новый объект с данными пользователя.'''
    form_class = AdditionsToTheProfileForm
    template_name = 'users/user_profile_create.html'
    pk_url_kwarg = 'username'

    def form_valid(self, form):
        '''Добавляет в форму пользователя.'''
        form.instance.user = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        '''Перенаправляет на страницу пользователя.'''
        return reverse_lazy(
            'users:user_profile',
            kwargs={'username': self.kwargs['username']})


class AdditionsToTheProfileUpdate(LoginRequiredMixin, DataMixin, UpdateView):
    '''Изменяет существующий объект с данными пользователя.'''
    form_class = AdditionsToTheProfileForm
    template_name = 'users/user_profile_create.html'
    pk_url_kwarg = 'profile_id'

    def form_valid(self, form):
        '''Добавляет в форму пользователя.'''
        form.instance.user = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        '''Перенаправляет на страницу пользователя.'''
        return reverse_lazy(
            'users:user_profile',
            kwargs={'username': self.request.user.username})
