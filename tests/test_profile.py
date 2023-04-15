import pytest
from django.contrib.auth import get_user_model


class TestProfileView:

    @pytest.mark.django_db(transaction=True)
    def test_profile_view_get(self, client, post_sale):
        url = f'/profile/{post_sale.author.username}'
        url_templ = '/profile/<username>/'
        try:
            response = client.get(url)
        except Exception as e:
            assert False, f'''Страница `{url_templ}` работает неправильно. Ошибка: `{e}`'''
        if response.status_code in (301, 302):
            response = client.get(f'{url}/')
        assert response.status_code != 404, (
            f'Страница `{url_templ}` не найдена, проверьте этот адрес в *urls.py*'
        )

        new_user = get_user_model()(username='new_user_87123478')
        new_user.save()
        url = f'/profile/{new_user.username}'
        try:
            new_response = client.get(url)
        except Exception as e:
            assert False, f'''Страница `{url_templ}` работает неправильно. Ошибка: `{e}`'''
        if new_response.status_code in (301, 302):
            new_response = client.get(f'{url}/')
