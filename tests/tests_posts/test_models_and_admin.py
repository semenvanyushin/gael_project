import pytest
from django.contrib.auth import get_user_model
from django.db.models import fields

from games.models import Account
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
