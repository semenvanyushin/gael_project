from django.urls import reverse_lazy
import pytest
from django import forms

from posts.models import PostSale
from posts.forms import PostSaleForm
from tests.utils import (check_delete_post_sale, get_field_from_context,
                         check_form_field)


class TestPostSaleView:

    @pytest.mark.django_db(transaction=True)
    def test_post_edit_view_author_get(self, user_client, post_sale):
        url = reverse_lazy('posts:post_edit', kwargs={'post_id': post_sale.id})
        try:
            response = user_client.get(url)
        except Exception as e:
            assert False, (
                f"Страница `{url}` работает неправильно. Ошибка: `{e}`"
            )
        if response.status_code in (301, 302):
            response = user_client.get(url)
        assert response.status_code != 404, (
            f'Страница `{url}` не найдена, проверьте этот адрес в *urls.py*'
        )

        post_context = get_field_from_context(response.context, PostSale)
        postform_context = get_field_from_context(
            response.context, PostSaleForm
        )
        assert any([post_context, postform_context]) is not None, (
            'Проверьте, что передали статью в контекст страницы '
            f'`{url}` типа `Post` или `PostForm`'
        )

        assert 'form' in response.context, (
            'Проверьте, что передали форму `form` '
            f'в контекст страницы `{url}`'
        )
        fields_cnt = 3
        assert len(response.context['form'].fields) == fields_cnt, (
            'Проверьте, что в форме `form` на страницу '
            f'`{url}` {fields_cnt} поля'
        )

        field_name = 'account'
        type_field = forms.models.ModelChoiceField
        check_form_field(response, field_name, url, type_field)

        field_name = 'price'
        type_field = forms.fields.IntegerField
        check_form_field(response, field_name, url, type_field)

        field_name = 'type_payment'
        type_field = forms.fields.CharField
        check_form_field(response, field_name, url, type_field)

    @pytest.mark.django_db(transaction=True)
    def test_post_edit_view_author_post(self, user_client, post_sale):
        price = 1000
        type_payment = 'Измененный вариант'
        url = reverse_lazy('posts:post_edit', kwargs={'post_id': post_sale.id})
        try:
            response = user_client.get(url)
        except Exception as e:
            assert False, (
                f"Страница `{url}` работает неправильно. Ошибка: `{e}`"
            )

        response = user_client.post(url, data={
            'price': price, 'account': post_sale.account_id,
            'type_payment': type_payment
        })

        assert response.status_code in (301, 302), (
            f'Проверьте, что со страницы `{url}` после создания поста '
            'перенаправляете на страницу пользователя'
        )
        post = PostSale.objects.filter(
            author=post_sale.author, price=price, account=post_sale.account
        ).first()
        assert post is not None, (
            'Проверьте, что вы изменили пост '
            f'при отправке формы на странице `{url}`'
        )
        assert response.url.startswith('/'), (
            'Проверьте, что перенаправляете на главную страницу `/`'
        )

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
