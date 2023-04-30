import tempfile

import pytest
from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UsernameField
from django.urls import reverse_lazy

from tests.utils import check_create_post, check_create_get
from users.models import AdditionsToTheProfile

User = get_user_model()


class TestUserCreateView:

    @pytest.mark.django_db(transaction=True)
    def test_create_view_get(self, client):
        url = reverse_lazy('users:signup')
        fields_cnt = 6
        fields = {
            'first_name': (forms.fields.CharField, True),
            'last_name': (forms.fields.CharField, True),
            'username': (UsernameField, True),
            'email': (forms.fields.EmailField, True)
        }
        check_create_get(client, url, fields_cnt, fields)

    @pytest.mark.django_db(transaction=True)
    def test_create_view_post(self, client):
        first_name = 'Имя'
        last_name = 'Фамилия'
        username = 'test'
        email = 'test@mail.ru'
        url = reverse_lazy('users:signup')
        redirect_url = reverse_lazy('users:login')
        response = client.post(url, data={
            'first_name': first_name, 'last_name': last_name,
            'username': username, 'email': email, 'password1': 'Komarovo2022!',
            'password2': 'Komarovo2022!'
        })
        created_object = User.objects.filter(
            first_name=first_name, last_name=last_name,
            username=username, email=email
        ).first()
        check_create_post(client, response, url,
                          redirect_url, created_object)


class TestUserProfileCreateView:

    @pytest.mark.django_db(transaction=True)
    def test_create_view_get(self, user_client, user):
        url = reverse_lazy('users:profile_create',
                           kwargs={'username': user.username})
        fields_cnt = 2
        fields = {
            'avatar': (forms.fields.ImageField, False,),
            'telegram': (forms.fields.CharField, False,)
        }
        check_create_get(user_client, url, fields_cnt, fields)

    @pytest.mark.django_db(transaction=True)
    def test_create_view_post(self, user_client, user):
        avatar = tempfile.NamedTemporaryFile(suffix=".jpg").name
        telegram = '@telegram'
        url = reverse_lazy('users:profile_create',
                           kwargs={'username': user.username})
        redirect_url = reverse_lazy(
            'users:user_profile', kwargs={'username': user.username})
        response = user_client.post(url, data={
            'avatar': avatar, 'telegram': telegram
        })
        created_object = AdditionsToTheProfile.objects.filter(
            user=user, telegram=telegram
        ).first()
        check_create_post(user_client, response, url,
                          redirect_url, created_object)
