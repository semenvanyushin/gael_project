import tempfile

import pytest
from mixer.backend.django import mixer as _mixer

from games.models import Account, Game, Owner
from posts.models import PostSale, Review


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


@pytest.fixture
def review(user, user_two):
    return Review.objects.create(
        user=user_two,
        author=user,
        score='PV',
        text='текст отзыва',
    )


@pytest.fixture
def few_posts_sale(mixer, user, game):
    posts = mixer.cycle(20).blend(PostSale, author=user, game=game)
    return posts[0]


@pytest.fixture
def few_review(mixer, user, user_two):
    review = mixer.cycle(20).blend(Review, user=user_two, author=user)
    return review[0]
