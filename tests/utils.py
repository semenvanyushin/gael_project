import re

from django.contrib.admin.sites import site
from django.core.paginator import Page, Paginator
from django.db.models import fields
from django.urls import reverse_lazy

from posts.models import PostSale, Review


def get_field_from_context(context, field_type):
    '''Возвращает поля формы.'''
    for field in context.keys():
        if field not in ('user', 'request') and isinstance(context[field],
                                                           field_type):
            return context[field]
    return


def search_field(fields, attname):
    '''Проверяет наличие поля в модели.'''
    for field in fields:
        if attname == field.attname:
            return field
    return None


def search_refind(execution, user_code):
    """Поиск запуска"""
    for temp_line in user_code.split('\n'):
        if re.search(execution, temp_line):
            return True
    return False


def admin_test(model, admin_fields, admin_search_fields, admin_list_filter):
    '''Проверяет поля, поиск и фильтры в админской панели'''
    admin_site = site

    assert model in admin_site._registry, (
        f'Зарегистрируйте модель `{model}` в админской панели'
    )

    admin_model = admin_site._registry[model]

    for field in admin_fields:
        assert field in admin_model.list_display, (
            f'Добавьте `{field}` для отображения в '
            'списке модели административного сайта'
        )

    for field in admin_search_fields:
        assert field in admin_model.search_fields, (
            f'Добавьте `{field}` для поиска модели административного сайта'
        )

    for filter in admin_list_filter:
        assert filter in admin_model.list_filter, (
            f'Добавьте `{filter}` для фильтрации '
            'модели административного сайта'
        )

    assert hasattr(admin_model, 'empty_value_display'), (
        'Добавьте дефолтное значение `-пусто-` для пустого поля'
    )
    assert admin_model.empty_value_display == '-пусто-', (
        'Добавьте дефолтное значение `-пусто-` для пустого поля'
    )


def check_field(model, model_fields, field_name, field_type, max_length=None,
                related_model=None, upload_to=None):
    '''Проверяет поле модели.'''
    field = search_field(model_fields, f'{field_name}')
    assert field is not None, (
        f'Добавьте свойство `{field_name}` в модель `{model}`'
    )
    assert type(field) == field_type, (
        f'Свойство `{field_name}` модели `{model}` должно быть `{field_type}`'
    )
    if type(field) == fields.related.ForeignKey:
        assert field.related_model == related_model, (
            f'Свойство `{field_name}` модели `{model}` '
            f'должно быть ссылкой на модель `{related_model}`'
        )
    if type(field) == fields.DateTimeField:
        assert field.auto_now_add, (
            f'Свойство `{field_name}` модели `{model}` '
            'должно быть `auto_now_add`'
        )
    if type(field) == fields.CharField:
        assert field.max_length == max_length, (
            f'Задайте максимальную длину `{field_name}` '
            f'модели `{model}` {max_length}'
        )
    if type(field) == fields.files.ImageField:
        assert field.upload_to == f'{upload_to}', (
            f"Свойство `{field_name}` модели `{model}` "
            f"должно быть с атрибутом `upload_to='{upload_to}'`"
        )


def check_form_field(response, field_name, link, type_field):
    '''Проверяет поля в форме.'''
    assert f'{field_name}' in response.context['form'].fields, (
        'Проверьте, что в форме `form` на '
        f'странице `{link}` есть поле `{field_name}`'
    )
    assert type(
        response.context['form'].fields[f'{field_name}']
    ) == type_field, (
        'Проверьте, что в форме `form` на странице '
        f'`{link}` поле `{field_name}` типа `{type_field}`'
    )
    assert response.context['form'].fields[f'{field_name}'].required, (
        'Проверьте, что в форме `form` на странице '
        f'`{link}` поле `{field_name}` обязательно'
    )


def url_paginator_view(client, data, url):
    '''Проверяет наличие пагинации на странице.'''
    response = client.get(url)
    assert response.status_code != 404, (
        f'Страница `{url}` не найдена, проверьте этот адрес в *urls.py*'
    )
    assert 'page_obj' in response.context, (
        'Проверьте, что передали переменную '
        f'`page_obj` в контекст страницы `{url}`'
    )
    assert isinstance(response.context['page_obj'], Page), (
        f'Проверьте, что переменная `page_obj` на странице `{url}` типа `Page`'
    )


def paginator_not_in_view_context(client, data, url):
    '''Проверяет соответствие переменной "paginator" типу "Paginator".'''
    response = client.get(url)
    assert isinstance(response.context['page_obj'].paginator, Paginator), (
        'Проверьте, что переменная `paginator` объекта `page_obj`'
        f' на странице `{url}` типа `Paginator`'
    )


def get_url_try(user, user_client, url):
    '''Проверяет доступность страницы на "get" запрос'''
    try:
        user_client.get(url)
    except Exception as e:
        assert False, (
            f'Страница `{url}` работает неправильно. Ошибка: `{e}`'
        )


def check_create_post(user_client, response, url,
                      redirect_url, created_object):
    '''Проверяет создание объекта через форму "post" запросом.'''
    assert response.status_code in (301, 302), (
        f'Проверьте, что со страницы {url} после создания поста, '
        f'перенаправляете на страницу `{redirect_url}`'
    )

    assert created_object is not None, (
        'Проверьте, что вы сохранили новый пост '
        f'при отправке формы на странице `{url}`'
    )
    assert response.url == redirect_url, (
        'Проверьте, что перенаправляете на страницу отзывов '
        f'на автора `{redirect_url}`'
    )

    response = user_client.post(url)
    assert response.status_code == 200, (
        f'Проверьте, что на странице {url} выводите ошибки '
        'при неправильной заполненной формы `form`'
    )


def check_create_get(user_client, url, fields_cnt, fields):
    '''Проверяет выдачу формы при "get" запросе.'''
    try:
        response = user_client.get(url)
    except Exception as e:
        assert False, (
            f"Страница '{url}' работает неправильно. Ошибка: `{e}`"
        )
    if response.status_code in (301, 302):
        response = user_client.get(url)
    assert response.status_code != 404, (
        f"Страница `{url}` не найдена, проверьте этот адрес в *urls.py*"
    )
    assert 'form' in response.context, (
        'Проверьте, что передали форму `form` '
        f'в контекст страницы `{url}`'
    )
    assert len(response.context['form'].fields) == fields_cnt, (
        'Проверьте, что в форме `form` '
        f'на страницу `{url}` {fields_cnt} поля'
    )

    for item in fields:
        check_form_field(response, item, url, fields[item])


def check_delete_review(user, user_two, client, finish_objects_count):
    '''Проверяет удаление отзыва и права на эту операцию.'''
    assert Review.objects.count() == 0
    review_for_delete = Review.objects.create(
        author=user, user=user_two, score='PV', text='текст отзыва'
    )
    assert Review.objects.count() == 1, (
        'Проверьте модель `Review`, не удается создать пост.'
    )
    url = reverse_lazy(
        'posts:review_delete',
        kwargs={'username': user_two.username,
                'review_id': review_for_delete.id}
    )
    response = client.post(url)
    assert response.status_code in (301, 302), (
        f'Проверьте, что со страницы `{url}` перенаправляете на страницу '
        'пользователя, если запрос не от автора поста'
    )
    assert Review.objects.count() == finish_objects_count, (
        'Проверьте, что только автор может удалить свой пост.'
    )


def check_delete_post_sale(user, account, client, finish_objects_count):
    '''Проверяет удаление поста и права на эту операцию.'''
    assert PostSale.objects.count() == 0
    post_for_delete = PostSale.objects.create(
        author=user, account=account,
        price=800, type_payment='вариант оплаты'
    )
    assert PostSale.objects.count() == 1, (
        'Проверьте модель `PostSale`, не удается создать пост.'
    )
    url = reverse_lazy(
        'posts:post_delete', kwargs={'post_id': post_for_delete.id}
    )
    response = client.post(url)
    assert response.status_code in (301, 302), (
        f'Проверьте, что со страницы `{url}` перенаправляете на страницу '
        'пользователя, если запрос не от автора поста'
    )
    assert PostSale.objects.count() == finish_objects_count, (
        'Проверьте, что только автор может удалить свой пост.'
    )
