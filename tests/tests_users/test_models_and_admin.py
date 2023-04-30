import tempfile

import pytest
from django.db.models import fields

from tests.utils import admin_test, check_field


try:
    from users.models import User
except ImportError:
    assert False, 'Не найдена модель User'
try:
    from users.models import AdditionsToTheProfile
except ImportError:
    assert False, 'Не найдена модель AdditionsToTheProfile'


class TestUser:

    def test_user_model(self):
        model = User
        model_fields = User._meta.fields
        field_name_and_type = {
            'email': (fields.EmailField, 255, True),
            'first_name': (fields.CharField, 255),
            'last_name': (fields.CharField, 255),
        }
        check_field(model, model_fields, **field_name_and_type)

    @pytest.mark.django_db(transaction=True)
    def test_user_create(self):
        email = 'test@mail.ru'
        first_name = 'Тестовое имя'
        last_name = 'Тестовая фамилия'
        assert User.objects.count() == 0
        test_user = User.objects.create(
            email=email, first_name=first_name, last_name=last_name)
        assert User.objects.count() == 1
        assert User.objects.get(
            email=email, first_name=first_name, last_name=last_name
        ).pk == test_user.pk

    def test_user_admin(self):
        model = User
        user_admin_fields = ('id', 'username', 'email', 'first_name',
                             'last_name', 'date_joined',)
        user_admin_search_fields = ('email', 'username', 'first_name',
                                    'last_name',)
        user_admin_list_filter = ('date_joined', 'email', 'first_name',)
        admin_test(model, user_admin_fields, user_admin_search_fields,
                   user_admin_list_filter)


class TestAdditionsToTheProfile:

    def test_user_profile_model(self):
        model = AdditionsToTheProfile
        model_fields = AdditionsToTheProfile._meta.fields
        field_name_and_type = {
            'avatar': (fields.files.ImageField, 'static/avatar/%Y/%m/%d/'),
            'telegram': (fields.CharField, 255),
        }
        check_field(model, model_fields, **field_name_and_type)

    @pytest.mark.django_db(transaction=True)
    def test_user_profile_create(self, user):
        avatar = tempfile.NamedTemporaryFile(suffix=".jpg").name
        telegram = '@test'
        assert AdditionsToTheProfile.objects.count() == 0
        test_user_profile = AdditionsToTheProfile.objects.create(
            user=user, avatar=avatar, telegram=telegram)
        assert AdditionsToTheProfile.objects.count() == 1
        assert AdditionsToTheProfile.objects.get(
            user=user, avatar=avatar, telegram=telegram
        ).pk == test_user_profile.pk

    def test_user_profile_admin(self):
        model = AdditionsToTheProfile
        user_profile_admin_fields = ('avatar_tag', 'user',)
        user_profile_admin_search_fields = ('user',)
        user_profile_admin_list_filter = ()
        admin_test(model, user_profile_admin_fields,
                   user_profile_admin_search_fields,
                   user_profile_admin_list_filter)
