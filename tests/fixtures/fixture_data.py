import tempfile

import pytest
from mixer.backend.django import mixer as _mixer

from games.models import Account, Game, Owner
from posts.models import PostSale


@pytest.fixture()
def mock_media(settings):
    with tempfile.TemporaryDirectory() as temp_directory:
        settings.MEDIA_ROOT = temp_directory
        yield temp_directory


@pytest.fixture
def mixer():
    return _mixer


@pytest.fixture
def account(user):
    logo_region = tempfile.NamedTemporaryFile(suffix=".jpg").name
    return Account.objects.create(
        organizer=user,
        login='game@mail.ru',
        store_region='вариант оплаты',
        logo_region=logo_region,
    )


@pytest.fixture
def owner(user, account):
    return Owner.objects.create(
        user=user,
        account=account,
        platform='PS5',
        type_activation='П4',
    )


@pytest.fixture
def game(owner):
    logo = tempfile.NamedTemporaryFile(suffix=".jpg").name
    return Game.objects.create(
        owner=owner,
        logo=logo,
        description='Описание игры',
        rating=8,
        release_date='01.01.2022',
    )


@pytest.fixture
def post_sale(user, game):
    return PostSale.objects.create(
        author=user,
        game=game,
        price=500,
        type_payment='вариант оплаты',
    )
