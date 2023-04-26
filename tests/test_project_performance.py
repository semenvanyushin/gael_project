import tempfile

import pytest
from django.contrib.auth import get_user_model
from django.db.models import fields

from tests.utils import admin_test, check_field


try:
    from posts.models import PostSale
except ImportError:
    assert False, 'Не найдена модель PostSale'
try:
    from posts.models import Review
except ImportError:
    assert False, 'Не найдена модель Review'
try:
    from posts.models import FavoritePost
except ImportError:
    assert False, 'Не найдена модель FavoritePost'

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


class TestPostSale:

    def test_post_sale_model(self):
        model = PostSale
        model_fields = PostSale._meta.fields

        field_name = 'price'
        field_type = fields.IntegerField
        check_field(model, model_fields, field_name, field_type)

        field_name = 'pub_date'
        field_type = fields.DateTimeField
        check_field(model, model_fields, field_name, field_type)

        field_name = 'author_id'
        related_model = get_user_model()
        field_type = fields.related.ForeignKey
        check_field(model, model_fields, field_name, field_type,
                    related_model=related_model)

        field_name = 'account_id'
        related_model = Account
        field_type = fields.related.ForeignKey
        check_field(model, model_fields, field_name, field_type,
                    related_model=related_model)

        field_name = 'type_payment'
        max_length = 255
        field_type = fields.CharField
        check_field(model, model_fields, field_name, field_type,
                    max_length=max_length)

    @pytest.mark.django_db(transaction=True)
    def test_post_sale_create(self, user, account):
        price = 1000
        type_payment = 'Вариант оплаты'
        assert PostSale.objects.count() == 0
        post_sale = PostSale.objects.create(
            price=price, author=user,
            account=account, type_payment=type_payment
        )
        assert PostSale.objects.count() == 1
        assert PostSale.objects.get(
            price=price, author=user,
            account=account, type_payment=type_payment
        ).pk == post_sale.pk

    def test_post_sale_admin(self):
        model = PostSale
        post_sale_admin_fields = (
            'get_username', 'get_account_login',
            'price', 'type_payment', 'pub_date'
        )
        post_sale_admin_search_fields = ('get_account_login', 'pub_date')
        post_sale_admin_list_filter = ('account', 'pub_date')
        admin_test(model, post_sale_admin_fields,
                   post_sale_admin_search_fields, post_sale_admin_list_filter)


class TestReview:

    def test_review_model(self):
        model = Review
        model_fields = Review._meta.fields

        field_name = 'pub_date'
        field_type = fields.DateTimeField
        check_field(model, model_fields, field_name, field_type)

        field_name = 'author_id'
        related_model = get_user_model()
        field_type = fields.related.ForeignKey
        check_field(model, model_fields, field_name, field_type,
                    related_model=related_model)

        field_name = 'user_id'
        related_model = get_user_model()
        field_type = fields.related.ForeignKey
        check_field(model, model_fields, field_name, field_type,
                    related_model=related_model)

        field_name = 'score'
        max_length = 2
        field_type = fields.CharField
        check_field(model, model_fields, field_name, field_type,
                    max_length=max_length)

        field_name = 'text'
        field_type = fields.TextField
        check_field(model, model_fields, field_name, field_type)

    @pytest.mark.django_db(transaction=True)
    def test_review_create(self, user, user_two):
        text = 'Тестовый текст'
        score = 'PV'
        assert Review.objects.count() == 0
        review = Review.objects.create(
            user=user_two, author=user, text=text, score=score
        )
        assert Review.objects.count() == 1
        assert Review.objects.get(
            user=user_two.id, author=user.id, text=text, score=score
        ).pk == review.pk

    def test_review_admin(self):
        model = Review
        review_admin_fields = (
            'id', 'get_user_username', 'get_author_username',
            'text', 'score', 'pub_date'
        )
        review_admin_search_fields = ('user', 'author', 'score')
        review_admin_list_filter = ('user', 'author', 'pub_date')
        admin_test(model, review_admin_fields,
                   review_admin_search_fields, review_admin_list_filter)


class TestFavoritePost:

    def test_favorite_post_model(self):
        model = FavoritePost
        model_fields = FavoritePost._meta.fields

        field_name = 'creation_date'
        field_type = fields.DateTimeField
        check_field(model, model_fields, field_name, field_type)

        field_name = 'user_id'
        related_model = get_user_model()
        field_type = fields.related.ForeignKey
        check_field(model, model_fields, field_name, field_type,
                    related_model=related_model)

    @pytest.mark.django_db(transaction=True)
    def test_favorite_post_create(self, user, post_sale):
        assert FavoritePost.objects.count() == 0
        favorite_post = FavoritePost()
        favorite_post.user = user
        favorite_post.save()
        favorite_post.post_sale.add(post_sale)
        favorite_post.save()
        assert FavoritePost.objects.count() == 1
        assert FavoritePost.objects.get(
            user=user, post_sale=post_sale).pk == favorite_post.pk

    def test_favorite_post_admin(self):
        model = FavoritePost
        favorite_post_admin_fields = (
            'get_username', 'get_post_sale', 'creation_date'
        )
        favorite_post_admin_search_fields = ('get_post_sale',)
        favorite_post_admin_list_filter = ('creation_date',)
        admin_test(model, favorite_post_admin_fields,
                   favorite_post_admin_search_fields,
                   favorite_post_admin_list_filter)


class TestGame:

    def test_game_model(self):
        model = Game
        model_fields = Game._meta.fields

        field_name = 'name'
        max_length = 255
        field_type = fields.CharField
        check_field(model, model_fields, field_name, field_type,
                    max_length=max_length)

        field_name = 'description'
        field_type = fields.TextField
        check_field(model, model_fields, field_name, field_type)

        field_name = 'release_date'
        max_length = 50
        field_type = fields.CharField
        check_field(model, model_fields, field_name, field_type,
                    max_length=max_length)

        field_name = 'logo'
        upload_to = 'static/logo/%Y/%m/%d/'
        field_type = fields.files.ImageField
        check_field(model, model_fields, field_name, field_type,
                    upload_to=upload_to)

        field_name = 'rating'
        field_type = fields.FloatField
        check_field(model, model_fields, field_name, field_type)

        field_name = 'creation_date'
        field_type = fields.DateTimeField
        check_field(model, model_fields, field_name, field_type)

    @pytest.mark.django_db(transaction=True)
    def test_game_create(self, owner):
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

        field_name = 'platform'
        max_length = 100
        field_type = fields.CharField
        check_field(model, model_fields, field_name, field_type,
                    max_length=max_length)

        field_name = 'type_activation'
        max_length = 10
        field_type = fields.CharField
        check_field(model, model_fields, field_name, field_type,
                    max_length=max_length)

        field_name = 'user_id'
        related_model = get_user_model()
        field_type = fields.related.ForeignKey
        check_field(model, model_fields, field_name, field_type,
                    related_model=related_model)

        field_name = 'creation_date'
        field_type = fields.DateTimeField
        check_field(model, model_fields, field_name, field_type)

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

        field_name = 'login'
        max_length = 255
        field_type = fields.CharField
        check_field(model, model_fields, field_name, field_type,
                    max_length=max_length)

        field_name = 'store_region'
        max_length = 50
        field_type = fields.CharField
        check_field(model, model_fields, field_name, field_type,
                    max_length=max_length)

        field_name = 'logo_region'
        upload_to = 'static/logo_region/%Y/%m/%d/'
        field_type = fields.files.ImageField
        check_field(model, model_fields, field_name, field_type,
                    upload_to=upload_to)

        field_name = 'organizer_id'
        related_model = get_user_model()
        field_type = fields.related.ForeignKey
        check_field(model, model_fields, field_name, field_type,
                    related_model=related_model)

        field_name = 'game_id'
        related_model = Game
        field_type = fields.related.ForeignKey
        check_field(model, model_fields, field_name, field_type,
                    related_model=related_model)

        field_name = 'creation_date'
        field_type = fields.DateTimeField
        check_field(model, model_fields, field_name, field_type)

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


class TestCustomErrorPages:

    @pytest.mark.django_db(transaction=True)
    def test_custom_404(self, client):
        url_invalid = '/some_invalid_url_404/'
        code = 404
        response = client.get(url_invalid)
        assert response.status_code == code, (
            'Убедитесь, что для несуществующих адресов страниц, '
            f'сервер возвращает код {code}'
        )
        try:
            from gael.urls import handler404
        except ImportError:
            assert False, (
                f'Убедитесь, что для страниц, возвращающих код {code}, '
                'настроен кастомный шаблон'
            )

    @pytest.mark.django_db(transaction=True)
    def test_custom_500(self):
        code = 500
        try:
            from gael.urls import handler500
        except ImportError:
            assert False, (
                f'Убедитесь, что для страниц, возвращающих код {code}, '
                'настроен кастомный шаблон'
            )

    @pytest.mark.django_db(transaction=True)
    def test_custom_403(self):
        code = 403
        try:
            from gael.urls import handler403
        except ImportError:
            assert False, (
                f'Убедитесь, что для страниц, возвращающих код {code}, '
                'настроен кастомный шаблон'
            )
