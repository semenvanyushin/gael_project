from django.urls import reverse_lazy
import pytest
from django import forms

from posts.models import PostSale
from posts.forms import PostSaleForm
from tests.utils import (check_delete_post_sale, post_edit_view_author_get,
                         try_get_url)


class TestPostSaleView:

    @pytest.mark.django_db(transaction=True)
    def test_post_edit_view_author_get(self, user_client, post_sale):
        url = reverse_lazy('posts:post_edit', kwargs={'post_id': post_sale.id})
        fields_cnt = 3
        model = PostSale
        form = PostSaleForm
        fields_data = {
            'account': (forms.models.ModelChoiceField, True),
            'price': (forms.fields.IntegerField, True),
            'type_payment': (forms.fields.CharField, True)
        }
        post_edit_view_author_get(model, form, fields_cnt, fields_data,
                                  user_client, url)

    @pytest.mark.django_db(transaction=True)
    def test_post_edit_view_author_post(self, user_client, post_sale):
        price = 1000
        type_payment = 'Измененный вариант'
        url = reverse_lazy('posts:post_edit', kwargs={'post_id': post_sale.id})
        try_get_url(user_client, url)
        response = user_client.post(url, data={
            'price': price, 'account': post_sale.account_id,
            'type_payment': type_payment
        })
        assert response.status_code in (301, 302), (
            f'Проверьте, что со страницы `{url}` после создания поста '
            'перенаправляете на страницу пользователя')
        post = PostSale.objects.filter(
            author=post_sale.author, price=price, account=post_sale.account
        ).first()
        assert post is not None, ('Проверьте, что вы изменили пост '
                                  f'при отправке формы на странице `{url}`')
        assert response.url.startswith('/'), (
            'Проверьте, что перенаправляете на главную страницу `/`')

    @pytest.mark.django_db(transaction=True)
    def test_post_delete_view_author_post(self, user, user_client, account):
        '''Проверяет удаление поста автором.'''
        client = user_client
        finish_objects_count = 0
        check_delete_post_sale(user, account, client, finish_objects_count)

    @pytest.mark.django_db(transaction=True)
    def test_post_delete_view_not_author_post(self, user,
                                              user_two_client, account):
        '''Проверяет удаление поста автора другим пользователем.'''
        client = user_two_client
        finish_objects_count = 1
        check_delete_post_sale(user, account, client, finish_objects_count)
