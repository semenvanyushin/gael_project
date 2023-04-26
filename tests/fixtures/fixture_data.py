import tempfile

import pytest
from mixer.backend.django import mixer as _mixer

from chats.models import Chat, Message
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
def owner(user):
    return Owner.objects.create(
        user=user,
        platform='PS5',
        type_activation='П4',
    )


@pytest.fixture
def game():
    logo = tempfile.NamedTemporaryFile(suffix=".jpg").name
    return Game.objects.create(
        logo=logo,
        description='Описание игры',
        rating=8,
        release_date='01.01.2022',
    )


@pytest.fixture
def account(user, owner, game):
    logo_region = tempfile.NamedTemporaryFile(suffix=".jpg").name
    account = Account.objects.create(
        organizer=user,
        game=game,
        login='game@mail.ru',
        store_region='вариант оплаты',
        logo_region=logo_region,
    )
    account.save()
    account.owners.add(owner)
    account.save()
    return account


@pytest.fixture
def post_sale(user, account):
    return PostSale.objects.create(
        author=user,
        account=account,
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
def chat(user, user_two):
    chat = Chat.objects.create(type='D')
    chat.save()
    chat.members.add(user)
    chat.save()
    chat.members.add(user_two)
    chat.save()
    return chat


@pytest.fixture
def message(chat, user):
    return Message.objects.create(
        chat=chat,
        author=user,
        message='Текст сообщения',
        text='текст отзыва',
    )


@pytest.fixture
def few_posts_sale(mixer, user, account):
    posts = mixer.cycle(20).blend(PostSale, author=user, account=account)
    return posts[0]


@pytest.fixture
def few_review(mixer, user, user_two):
    review = mixer.cycle(20).blend(Review, user=user_two, author=user)
    return review[0]
