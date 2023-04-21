import pytest


@pytest.fixture
def user(django_user_model):
    return django_user_model.objects.create_user(
        username='test_user',
        email='test@mail.ru',
        first_name='name',
        last_name='surname',
    )


@pytest.fixture
def user_two(django_user_model):
    return django_user_model.objects.create_user(
        username='test_user_two',
        email='test_two@mail.ru',
        first_name='name_two',
        last_name='surname_two',
    )


@pytest.fixture
def user_client(user, client):
    client.force_login(user)
    return client


@pytest.fixture
def user_two_client(user_two, client):
    client.force_login(user_two)
    return client


@pytest.fixture
def another_user(mixer):
    from django.contrib.auth.models import User
    return mixer.blend(User, username='AnotherUser')
