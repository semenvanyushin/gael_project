import pytest
from django import forms

from posts.models import PostSale, Review


def checklist_field(response, field_name, link, type_field):
    assert f'{field_name}' in response.context['form'].fields, (
        f'Проверьте, что в форме `form` на странице `{link}` есть поле `{field_name}`'
    )
    assert type(response.context['form'].fields[f'{field_name}']) == type_field, (
        f'Проверьте, что в форме `form` на странице `{link}` поле `{field_name}` типа `{type_field}`'
    )
    assert response.context['form'].fields[f'{field_name}'].required, (
        f'Проверьте, что в форме `form` на странице `{link}` поле `{field_name}` обязательно'
    )


class TestPostSaleCreateView:

    @pytest.mark.django_db(transaction=True)
    def test_create_view_get(self, user_client):
        link = '/create/'
        try:
            response = user_client.get('/create/')
        except Exception as e:
            assert False, f'''Страница `/create/` работает неправильно. Ошибка: `{e}`'''
        if response.status_code in (301, 302):
            response = user_client.get('/create/')
        assert response.status_code != 404, 'Страница `/create/` не найдена, проверьте этот адрес в *urls.py*'
        assert 'form' in response.context, 'Проверьте, что передали форму `form` в контекст страницы `/create/`'
        fields_cnt = 3
        assert len(response.context['form'].fields) == fields_cnt, (
            f'Проверьте, что в форме `form` на страницу `/create/` {fields_cnt} поля'
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
    def test_create_view_post(self, user_client, user, game):
        price = 1000
        type_payment = 'Вариант оплаты'
        try:
            response = user_client.get('/create')
        except Exception as e:
            assert False, f'''Страница `/create` работает неправильно. Ошибка: `{e}`'''
        url = '/create/' if response.status_code in (301, 302) else '/create'

        response = user_client.post(url, data={'price': price, 'game': game.id, 'type_payment': type_payment})

        assert response.status_code in (301, 302), (
            'Проверьте, что со страницы `/create/` после создания поста, '
            f'перенаправляете на страницу профиля автора `/profile/{user.username}`'
        )
        post = PostSale.objects.filter(author=user, price=price, game=game, type_payment=type_payment).first()
        assert post is not None, 'Проверьте, что вы сохранили новый пост при отправки формы на странице `/create/`'
        assert response.url == f'/profile/{user.username}/', (
            f'перенаправляете на страницу профиля автора `/profile/{user.username}`'
        )

        response = user_client.post(url)
        assert response.status_code == 200, (
            'Проверьте, что на странице `/create/` выводите ошибки при неправильной заполненной формы `form`'
        )


class TestReviewCreateView:

    @pytest.mark.django_db(transaction=True)
    def test_create_view_get(self, user_client, user):
        link = f'/profile/{user.username}/reviews/create/'
        try:
            response = user_client.get(link)
        except Exception as e:
            assert False, f'''Страница '{link}' работает неправильно. Ошибка: `{e}`'''
        if response.status_code in (301, 302):
            response = user_client.get(link)
        assert response.status_code != 404, f'''Страница `{link}` не найдена, проверьте этот адрес в *urls.py*'''
        assert 'form' in response.context, f'''Проверьте, что передали форму `form` в контекст страницы `{link}`'''
        fields_cnt = 2
        assert len(response.context['form'].fields) == fields_cnt, (
            f'''Проверьте, что в форме `form` на страницу `{link}` {fields_cnt} поля'''
        )

        field_name = 'text'
        type_field = forms.fields.CharField
        checklist_field(response, field_name, link, type_field)

        field_name = 'score'
        type_field = forms.fields.TypedChoiceField
        checklist_field(response, field_name, link, type_field)

    @pytest.mark.django_db(transaction=True)
    def test_create_view_post(self, user_client, user, user_two):
        text = 'Текст отзыва'
        score = 'PV'
        url = f'/profile/{user_two.username}/reviews/create/'
        try:
            response = user_client.get(url)
        except Exception as e:
            assert False, f'''Страница `{url}` работает неправильно. Ошибка: `{e}`'''

        response = user_client.post(url, data={'text': text, 'score': score})

        assert response.status_code in (301, 302), (
            f'''Проверьте, что со страницы {url} после создания поста, '''
            f'перенаправляете на страницу профиля автора `profile/{user_two.username}/reviews/`'
        )
        review = Review.objects.filter(author=user, text=text, score=score).first()
        assert review is not None, f'''Проверьте, что вы сохранили новый пост при отправке формы на странице `{url}`'''
        assert response.url == f'/profile/{user_two.username}/reviews/', (
            f'перенаправляете на страницу отзывов на автора `profile/{user_two.username}/reviews/`'
        )

        response = user_client.post(url)
        assert response.status_code == 200, (
            f'''Проверьте, что на странице {url} выводите ошибки при неправильной заполненной формы `form`'''
        )
