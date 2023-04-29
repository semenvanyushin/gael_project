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


def try_get_url(client, url):
    '''Проверяет доступность url по запросу get'''
    try:
        return client.get(url)
    except Exception as e:
        assert False, (f"Страница `{url}` работает неправильно. Ошибка: `{e}`")


def admin_test(model, admin_fields, admin_search_fields, admin_list_filter):
    '''Проверяет поля, поиск и фильтры в админской панели'''
    admin_site = site
    assert model in admin_site._registry, (
        f'Зарегистрируйте модель `{model}` в админской панели')
    admin_model = admin_site._registry[model]
    for field in admin_fields:
        assert field in admin_model.list_display, (
            f'Добавьте `{field}` для отображения в '
            'списке модели административного сайта')
    for field in admin_search_fields:
        assert field in admin_model.search_fields, (
            f'Добавьте `{field}` для поиска модели административного сайта')
    for filter in admin_list_filter:
        assert filter in admin_model.list_filter, (
            f'Добавьте `{filter}` для фильтрации '
            'модели административного сайта')
    assert hasattr(admin_model, 'empty_value_display'), (
        'Добавьте дефолтное значение `-пусто-` для пустого поля')
    assert admin_model.empty_value_display == '-пусто-', (
        'Добавьте дефолтное значение `-пусто-` для пустого поля')


def check_field(model, model_fields, **kwargs):
    '''Проверяет поле модели.'''
    for key, value in kwargs.items():
        field = search_field(model_fields, f'{key}')
        assert field is not None, (
            f'Добавьте свойство `{key}` в модель `{model}`')
        assert type(field) == value[0], (
            f'Свойство `{key}` модели `{model}` должно быть `{value[0]}`')
        if type(field) == fields.related.ForeignKey:
            assert field.related_model == value[1], (
                f'Свойство `{key}` модели `{model}` '
                f'должно быть ссылкой на модель `{value[1]}`')
        if type(field) == fields.DateTimeField:
            assert field.auto_now_add, (
                f'Свойство `{key}` модели `{model}` '
                'должно быть `auto_now_add`')
        if type(field) == fields.CharField:
            assert field.max_length == value[1], (
                f'Задайте максимальную длину `{key}` '
                f'модели `{model}` {value[1]}')
        if type(field) == fields.files.ImageField:
            assert field.upload_to == f'{value[1]}', (
                f"Свойство `{key}` модели `{model}` "
                f"должно быть с атрибутом `upload_to='{value[1]}'`")


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


def post_edit_view_author_get(model, form, fields_cnt, fields_data,
                              client, url):
    '''Проверяет работу формы.'''
    response = try_get_url(client, url)
    assert response.status_code != 404, (
        f'Страница `{url}` не найдена, проверьте этот адрес в *urls.py*')
    post_context = get_field_from_context(response.context, model)
    postform_context = get_field_from_context(response.context, form)
    assert any([post_context, postform_context]) is not None, (
        'Проверьте, что передали в контекст страницы '
        f'`{url}` типа `Post` или `PostForm`')
    assert 'form' in response.context, (
        'Проверьте, что передали форму `form` '
        f'в контекст страницы `{url}`')
    assert len(response.context['form'].fields) == fields_cnt, (
        'Проверьте, что в форме `form` на страницу '
        f'`{url}` {fields_cnt} поля')
    for field_name, type_field in fields_data.items():
        check_form_field(response, field_name, url, type_field)


def url_paginator_view(client, url):
    '''Проверяет наличие пагинации на странице.'''
    response = try_get_url(client, url)
    assert response.status_code != 404, (
        f'Страница `{url}` не найдена, проверьте этот адрес в *urls.py*')
    assert 'page_obj' in response.context, (
        'Проверьте, что передали переменную '
        f'`page_obj` в контекст страницы `{url}`')
    assert isinstance(response.context['page_obj'], Page), (
        f'Проверьте, что переменная `page_obj` на странице `{url}` типа `Page`'
    )


def paginator_not_in_view_context(client, url):
    '''Проверяет соответствие переменной "paginator" типу "Paginator".'''
    response = try_get_url(client, url)
    assert isinstance(response.context['page_obj'].paginator, Paginator), (
        'Проверьте, что переменная `paginator` объекта `page_obj`'
        f' на странице `{url}` типа `Paginator`')


def check_create_post(user_client, response, url,
                      redirect_url, created_object):
    '''Проверяет создание объекта через форму "post" запросом.'''
    try_get_url(user_client, url)
    assert response.status_code in (301, 302), (
        f'Проверьте, что со страницы {url} после создания поста, '
        f'перенаправляете на страницу `{redirect_url}`')
    assert created_object is not None, (
        'Проверьте, что вы сохранили новый пост '
        f'при отправке формы на странице `{url}`')
    assert response.url == redirect_url, (
        'Проверьте, что перенаправляете на страницу отзывов '
        f'на автора `{redirect_url}`')
    response = user_client.post(url)
    assert response.status_code == 200, (
        f'Проверьте, что на странице {url} выводите ошибки '
        'при неправильной заполненной формы `form`')


def check_create_get(user_client, url, fields_cnt, fields):
    '''Проверяет выдачу формы при "get" запросе.'''
    response = try_get_url(user_client, url)
    assert response.status_code != 404, (
        f"Страница `{url}` не найдена, проверьте этот адрес в *urls.py*")
    assert 'form' in response.context, (
        f'Проверьте, что передали форму `form` в контекст страницы `{url}`')
    assert len(response.context['form'].fields) == fields_cnt, (
        f'Проверьте, что в форме `form` на страницу `{url}` {fields_cnt} поля')
    for field, field_type in fields.items():
        check_form_field(response, field, url, field_type)


def check_delete_review(user, user_two, client, finish_objects_count):
    '''Проверяет удаление отзыва и права на эту операцию.'''
    assert Review.objects.count() == 0
    review_for_delete = Review.objects.create(
        author=user, user=user_two, score='PV', text='текст отзыва')
    assert Review.objects.count() == 1, (
        'Проверьте модель `Review`, не удается создать пост.')
    url = reverse_lazy(
        'posts:review_delete',
        kwargs={'username': user_two.username,
                'review_id': review_for_delete.id})
    response = client.post(url)
    assert response.status_code in (301, 302), (
        f'Проверьте, что со страницы `{url}` перенаправляете на страницу '
        'пользователя, если запрос не от автора поста')
    assert Review.objects.count() == finish_objects_count, (
        'Проверьте, что только автор может удалить свой пост.')


def check_delete_post_sale(user, account, client, finish_objects_count):
    '''Проверяет удаление поста и права на эту операцию.'''
    assert PostSale.objects.count() == 0
    post_for_delete = PostSale.objects.create(
        author=user, account=account, price=800, type_payment='вариант оплаты')
    assert PostSale.objects.count() == 1, (
        'Проверьте модель `PostSale`, не удается создать пост.')
    url = reverse_lazy(
        'posts:post_delete', kwargs={'post_id': post_for_delete.id})
    response = client.post(url)
    assert response.status_code in (301, 302), (
        f'Проверьте, что со страницы `{url}` перенаправляете на страницу '
        'пользователя, если запрос не от автора поста')
    assert PostSale.objects.count() == finish_objects_count, (
        'Проверьте, что только автор может удалить свой пост.')
