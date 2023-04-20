import pytest
from django import forms

from posts.models import PostSale
from posts.forms import PostSaleForm
from tests.utils import get_field_from_context
from tests.utils import checklist_field


class TestPostSaleView:

    @pytest.mark.django_db(transaction=True)
    def test_post_edit_view_author_get(self, user_client, post_sale):
        link = f'/posts/{post_sale.id}/edit/'
        try:
            response = user_client.get(link)
        except Exception as e:
            assert False, (
                f"Страница `{link}` работает неправильно. Ошибка: `{e}`"
            )
        if response.status_code in (301, 302):
            response = user_client.get(link)
        assert response.status_code != 404, (
            f'Страница `{link}` не найдена, проверьте этот адрес в *urls.py*'
        )

        post_context = get_field_from_context(response.context, PostSale)
        postform_context = get_field_from_context(
            response.context, PostSaleForm
        )
        assert any([post_context, postform_context]) is not None, (
            'Проверьте, что передали статью в контекст страницы '
            f'`{link}` типа `Post` или `PostForm`'
        )

        assert 'form' in response.context, (
            'Проверьте, что передали форму `form` '
            f'в контекст страницы `{link}`'
        )
        fields_cnt = 3
        assert len(response.context['form'].fields) == fields_cnt, (
            'Проверьте, что в форме `form` на страницу '
            f'`{link}` {fields_cnt} поля'
        )

        field_name = 'game'
        type_field = forms.models.ModelChoiceField
        checklist_field(response, field_name, link, type_field)

        field_name = 'price'
        type_field = forms.fields.IntegerField
        checklist_field(response, field_name, link, type_field)

        field_name = 'type_payment'
        type_field = forms.fields.CharField
        checklist_field(response, field_name, link, type_field)

    @pytest.mark.django_db(transaction=True)
    def test_post_edit_view_author_post(self, user_client, post_sale):
        price = 1000
        type_payment = 'Измененный вариант'
        link = f'/posts/{post_sale.id}/edit/'
        try:
            response = user_client.get(link)
        except Exception as e:
            assert False, (
                f"Страница `{link}` работает неправильно. Ошибка: `{e}`"
            )

        response = user_client.post(link, data={
            'price': price, 'game': post_sale.game_id,
            'type_payment': type_payment
        })

        assert response.status_code in (301, 302), (
            f'Проверьте, что со страницы `{link}` после создания поста '
            'перенаправляете на страницу пользователя'
        )
        post = PostSale.objects.filter(
            author=post_sale.author, price=price, game=post_sale.game
        ).first()
        assert post is not None, (
            'Проверьте, что вы изменили пост '
            f'при отправке формы на странице `{link}`'
        )
        assert response.url.startswith('/'), (
            'Проверьте, что перенаправляете на главную страницу `/`'
        )
