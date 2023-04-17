import re

from django.contrib.admin.sites import site
from django.db.models import fields


def get_field_from_context(context, field_type):
    for field in context.keys():
        if field not in ('user', 'request') and isinstance(context[field], field_type):
            return context[field]
    return


def search_field(fields, attname):
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
    admin_site = site

    assert model in admin_site._registry, f'Зарегистрируйте модель `{model}` в админской панели'

    admin_model = admin_site._registry[model]

    for field in admin_fields:
        assert field in admin_model.list_display, (
            f'Добавьте `{field}` для отображения в списке модели административного сайта'
        )

    for field in admin_search_fields:
        assert field in admin_model.search_fields, (
            f'Добавьте `{field}` для поиска модели административного сайта'
        )

    for filter in admin_list_filter:
        assert filter in admin_model.list_filter, (
            f'Добавьте `{filter}` для фильтрации модели административного сайта'
        )

    assert hasattr(admin_model, 'empty_value_display'), (
        'Добавьте дефолтное значение `-пусто-` для пустого поля'
    )
    assert admin_model.empty_value_display == '-пусто-', (
        'Добавьте дефолтное значение `-пусто-` для пустого поля'
    )


def created_date_field(model, model_fields, field_name):
    created = search_field(model_fields, f'{field_name}')
    assert created is not None, (
        f'Добавьте дату и время проведения события в `{field_name}` модели `{model}`'
    )
    assert type(created) == fields.DateTimeField, (
        f'Свойство `{field_name}` модели `{model}` должно быть датой и временем `DateTimeField`'
    )
    assert created.auto_now_add, (
        f'Свойство `{field_name}` модели `{model}` должно быть `auto_now_add`'
    )


def field_with_foregin_key(model, model_fields, field_name, related_model):
    field = search_field(model_fields, f'{field_name}')
    assert field is not None, f'Добавьте свойство `{field_name}` в модель `{model}`'
    assert type(field) == fields.related.ForeignKey, (
        f'Свойство `{field_name}` модели `{model}` должно быть ссылкой на другую модель `ForeignKey`'
    )
    assert field.related_model == related_model, (
        f'Свойство `{field_name}` модели `{model}` должно быть ссылкой на модель `{related_model}`'
    )


def char_field(model, model_fields, field_name, max_length):
    field = search_field(model_fields, f'{field_name}')
    assert field is not None, f'Добавьте свойство `{field_name}` в модель `{model}`'
    assert type(field) == fields.CharField, (
        f'Свойство `{field_name}` модели `{model}` должно быть `CharField`'
    )
    assert field.max_length == max_length, f'Задайте максимальную длину `{field_name}` модели `{model}` {max_length}'


def image_field(model, model_fields, field_name, upload_to):
    field = search_field(model_fields, f'{field_name}')
    assert field is not None, f'Добавьте свойство `{field_name}` в модель `{model}`'
    assert type(field) == fields.files.ImageField, (
        f'Свойство `{field_name}` модели `{model}` должно быть `ImageField`'
    )
    assert field.upload_to == f'{upload_to}', (
        f"Свойство `{field_name}` модели `{model}` должно быть с атрибутом `upload_to='{upload_to}'`"
    )


def text_field(model, model_fields, field_name):
    field = search_field(model_fields, f'{field_name}')
    assert field is not None, f'Добавьте свойство `{field_name}` в модель `{model}`'
    assert type(field) == fields.TextField, (
        f'Свойство `{field_name}` модели `{model}` должно быть `TextField`'
    )


def integer_field(model, model_fields, field_name):
    field = search_field(model_fields, f'{field_name}')
    assert field is not None, f'Добавьте название события `{field_name}` модели `{model}`'
    assert type(field) == fields.IntegerField, (
        f'Свойство `{field_name}` модели `{model}` должно быть целым числом `IntegerField`'
    )


def float_field(model, model_fields, field_name):
    field = search_field(model_fields, f'{field_name}')
    assert field is not None, f'Добавьте свойство `{field_name}` модели `{model}`'
    assert type(field) == fields.FloatField, (
        f'Свойство `{field_name}` модели `{model}` должно быть числом `FloatField`'
    )


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
