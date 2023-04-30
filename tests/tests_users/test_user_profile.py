import tempfile

import pytest
from django import forms
from django.urls import reverse_lazy

from tests.utils import post_edit_view_author_get, try_get_url
from users.forms import AdditionsToTheProfileForm
from users.models import AdditionsToTheProfile


class TestUserProfileView:

    @pytest.mark.django_db(transaction=True)
    def test_user_profile_view_get(self, user_client, user_profile):
        url = reverse_lazy('users:profile_edit',
                           kwargs={'profile_id': user_profile.id})
        fields_cnt = 2
        model = AdditionsToTheProfile
        form = AdditionsToTheProfileForm
        fields_data = {
            'avatar': (forms.fields.ImageField, False),
            'telegram': (forms.fields.CharField, False),
        }
        post_edit_view_author_get(model, form, fields_cnt, fields_data,
                                  user_client, url)

    @pytest.mark.django_db(transaction=True)
    def test_user_profile_view_post(self, user_client, user_profile, user):
        avatar = tempfile.NamedTemporaryFile(suffix=".jpg").name
        telegram = '@testtest'
        url = reverse_lazy(
            'users:profile_edit',
            kwargs={'profile_id': user_profile.id})
        redirect_url = '/auth/profile/test_user/'
        try_get_url(user_client, url)
        response = user_client.post(url, data={'avatar': avatar,
                                               'telegram': telegram})
        assert response.status_code in (301, 302), (
            f'Проверьте, что со страницы `{url}` после создания поста '
            'перенаправляете на страницу пользователя')
        user_profile = AdditionsToTheProfile.objects.filter(
            user=user, telegram=telegram).first()
        assert user_profile is not None, (
            f'Проверьте, что вы изменили пост при отправке формы на `{url}`')
        assert response.url.startswith(redirect_url), (
            'Проверьте, что перенаправляете на страницу профиля '
            f'`{redirect_url}`')
