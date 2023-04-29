import pytest
from django.contrib.auth import get_user_model

from tests.utils import try_get_url


class TestProfileView:

    @pytest.mark.django_db(transaction=True)
    def test_profile_view_get(self, client, post_sale):
        url = f'/profile/{post_sale.author.username}/'
        url_templ = '/profile/<username>/'
        response = try_get_url(client, url)
        assert response.status_code != 404, (
            f'Страница `{url_templ}` не найдена, '
            'проверьте этот адрес в *urls.py*'
        )

        new_user = get_user_model()(username='new_user_87123478')
        new_user.save()
        url = f'/profile/{new_user.username}/'
        try_get_url(client, url)
