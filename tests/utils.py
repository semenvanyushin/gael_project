import re

from django.contrib.admin.sites import site
from django.core.paginator import Page, Paginator
from django.db.models import fields


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


def created_date_field(model, model_fields, field_name):
    '''Проверяет поле с датой и временем.'''
    created = search_field(model_fields, f'{field_name}')
    assert created is not None, (
        'Добавьте дату и время проведения события '
        f'в `{field_name}` модели `{model}`'
    )
    assert type(created) == fields.DateTimeField, (
        f'Свойство `{field_name}` модели `{model}` '
        'должно быть датой и временем `DateTimeField`'
    )
    assert created.auto_now_add, (
        f'Свойство `{field_name}` модели `{model}` должно быть `auto_now_add`'
    )


def field_with_foregin_key(model, model_fields, field_name, related_model):
    '''Проверяет поле со связью один ко многим.'''
    field = search_field(model_fields, f'{field_name}')
    assert field is not None, (
        f'Добавьте свойство `{field_name}` в модель `{model}`'
    )
    assert type(field) == fields.related.ForeignKey, (
        f'Свойство `{field_name}` модели `{model}` '
        'должно быть ссылкой на другую модель `ForeignKey`'
    )
    assert field.related_model == related_model, (
        f'Свойство `{field_name}` модели `{model}` '
        f'должно быть ссылкой на модель `{related_model}`'
    )


def char_field(model, model_fields, field_name, max_length):
    '''Проверяет поле текста с ограниением количества символов.'''
    field = search_field(model_fields, f'{field_name}')
    assert field is not None, (
        f'Добавьте свойство `{field_name}` в модель `{model}`'
    )
    assert type(field) == fields.CharField, (
        f'Свойство `{field_name}` модели `{model}` должно быть `CharField`'
    )
    assert field.max_length == max_length, (
        f'Задайте максимальную длину `{field_name}` '
        f'модели `{model}` {max_length}'
    )


def image_field(model, model_fields, field_name, upload_to):
    '''Проверяет поле с изображением.'''
    field = search_field(model_fields, f'{field_name}')
    assert field is not None, (
        f'Добавьте свойство `{field_name}` в модель `{model}`'
    )
    assert type(field) == fields.files.ImageField, (
        f'Свойство `{field_name}` модели `{model}` должно быть `ImageField`'
    )
    assert field.upload_to == f'{upload_to}', (
        f"Свойство `{field_name}` модели `{model}` "
        f"должно быть с атрибутом `upload_to='{upload_to}'`"
    )


def text_field(model, model_fields, field_name):
    '''Проверяет текстовое поле.'''
    field = search_field(model_fields, f'{field_name}')
    assert field is not None, (
        f'Добавьте свойство `{field_name}` в модель `{model}`'
    )
    assert type(field) == fields.TextField, (
        f'Свойство `{field_name}` модели `{model}` должно быть `TextField`'
    )


def integer_field(model, model_fields, field_name):
    '''Проверяет поле целым числом.'''
    field = search_field(model_fields, f'{field_name}')
    assert field is not None, (
        f'Добавьте название события `{field_name}` модели `{model}`'
    )
    assert type(field) == fields.IntegerField, (
        f'Свойство `{field_name}` модели `{model}` '
        'должно быть целым числом `IntegerField`'
    )


def float_field(model, model_fields, field_name):
    '''Проверяет поле с дробным числом.'''
    field = search_field(model_fields, f'{field_name}')
    assert field is not None, (
        f'Добавьте свойство `{field_name}` модели `{model}`'
    )
    assert type(field) == fields.FloatField, (
        f'Свойство `{field_name}` модели `{model}` '
        'должно быть числом `FloatField`'
    )


def checklist_field(response, field_name, link, type_field):
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
        checklist_field(response, item, url, fields[item])
