import tempfile

import pytest
from django.contrib.auth import get_user_model
from django.db.models import fields

from tests.utils import admin_test, check_field


try:
    from games.models import Game
except ImportError:
    assert False, 'Не найдена модель Game'
try:
    from games.models import Account
except ImportError:
    assert False, 'Не найдена модель Account'
try:
    from games.models import Owner
except ImportError:
    assert False, 'Не найдена модель Owner'


class TestGame:

    def test_game_model(self):
        model = Game
        model_fields = Game._meta.fields
        field_name_and_type = {
            'rating': (fields.FloatField,),
            'creation_date': (fields.DateTimeField,),
            'name': (fields.CharField, 255),
            'description': (fields.TextField,),
            'release_date': (fields.CharField, 50),
            'logo': (fields.files.ImageField, 'static/logo/%Y/%m/%d/'),
        }
        check_field(model, model_fields, **field_name_and_type)

    @pytest.mark.django_db(transaction=True)
    def test_game_create(self):
        name = 'Название игры'
        description = 'Описание игры'
        rating = 10
        release_date = '01.01.2019'
        assert Game.objects.count() == 0
        logo = tempfile.NamedTemporaryFile(suffix=".jpg").name
        game = Game.objects.create(
            name=name, description=description, rating=rating,
            release_date=release_date, logo=logo
        )
        assert Game.objects.count() == 1
        assert Game.objects.get(
            name=name, description=description, rating=rating,
            release_date=release_date, logo=logo
        ).pk == game.pk

    def test_game_admin(self):
        model = Game
        game_admin_fields = (
            'name', 'description', 'rating',
            'release_date', 'creation_date'
        )
        game_admin_search_fields = ('name', 'creation_date')
        game_admin_list_filter = ('name', 'creation_date')
        admin_test(model, game_admin_fields,
                   game_admin_search_fields, game_admin_list_filter)


class TestOwner:

    def test_owner_model(self):
        model = Owner
        model_fields = Owner._meta.fields
        field_name_and_type = {
            'platform': (fields.CharField, 100),
            'creation_date': (fields.DateTimeField,),
            'type_activation': (fields.CharField, 10),
            'user_id': (fields.related.ForeignKey, get_user_model()),
        }
        check_field(model, model_fields, **field_name_and_type)

    @pytest.mark.django_db(transaction=True)
    def test_owner_create(self, user):
        platform = 'Playstation 5'
        type_activation = 'П4'
        assert Owner.objects.count() == 0
        owner = Owner.objects.create(
            platform=platform, type_activation=type_activation, user=user
        )
        assert Owner.objects.count() == 1
        assert Owner.objects.get(
            platform=platform, type_activation=type_activation, user=user
        ).pk == owner.pk

    def test_owner_admin(self):
        model = Owner
        owner_admin_fields = (
            'get_username', 'platform',
            'type_activation', 'creation_date'
        )
        owner_admin_search_fields = ('get_username',)
        owner_admin_list_filter = ('creation_date',)
        admin_test(model, owner_admin_fields,
                   owner_admin_search_fields, owner_admin_list_filter)


class TestAccount:

    def test_account_model(self):
        model = Account
        model_fields = Account._meta.fields
        field_name_and_type = {
            'login': (fields.CharField, 255),
            'creation_date': (fields.DateTimeField,),
            'store_region': (fields.CharField, 50),
            'organizer_id': (fields.related.ForeignKey, get_user_model()),
            'game_id': (fields.related.ForeignKey, Game),
            'logo_region': (fields.files.ImageField,
                            'static/logo_region/%Y/%m/%d/'),
        }
        check_field(model, model_fields, **field_name_and_type)

    @pytest.mark.django_db(transaction=True)
    def test_account_create(self, user, game, owner):
        login = 'login@mail.ru'
        store_region = 'Турция'
        assert Account.objects.count() == 0
        logo_region = tempfile.NamedTemporaryFile(suffix=".jpg").name
        account = Account.objects.create(
            organizer=user, login=login,
            store_region=store_region, logo_region=logo_region,
            game=game
        )
        account.save()
        account.owners.add(owner)
        account.save()
        assert Account.objects.count() == 1
        assert Account.objects.get(
            organizer=user, login=login,
            store_region=store_region, logo_region=logo_region,
            game=game, owners=owner
        ).pk == account.pk

    def test_account_admin(self):
        model = Account
        account_admin_fields = (
            'get_organizer_username', 'get_owners', 'get_game_name',
            'login', 'store_region', 'creation_date'
        )
        account_admin_search_fields = ('login',)
        account_admin_list_filter = ('store_region', 'creation_date')
        admin_test(model, account_admin_fields,
                   account_admin_search_fields, account_admin_list_filter)
