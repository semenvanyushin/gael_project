import pytest
from django import forms

from posts.models import PostSale, Review
from tests.utils import check_create_post, check_create_get


class TestPostSaleCreateView:

    @pytest.mark.django_db(transaction=True)
    def test_create_view_get(self, user_client):
        url = '/create/'
        fields_cnt = 3
        fields = {
            'account': (forms.models.ModelChoiceField, True),
            'price': (forms.fields.IntegerField, True),
            'type_payment': (forms.fields.CharField, True)
        }
        check_create_get(user_client, url, fields_cnt, fields)

    @pytest.mark.django_db(transaction=True)
    def test_create_view_post(self, user_client, user, account):
        price = 1000
        type_payment = 'Вариант оплаты'
        url = '/create/'
        redirect_url = f'/profile/{user.username}/'
        response = user_client.post(url, data={
            'price': price, 'account': account.id, 'type_payment': type_payment
        })
        created_object = PostSale.objects.filter(
            author=user, price=price, account=account,
            type_payment=type_payment
        ).first()
        check_create_post(user_client, response, url,
                          redirect_url, created_object)


class TestReviewCreateView:

    @pytest.mark.django_db(transaction=True)
    def test_create_view_get(self, user_client, user):
        url = f'/profile/{user.username}/reviews/create/'
        fields_cnt = 2
        fields = {
            'text': (forms.fields.CharField, True),
            'score': (forms.fields.TypedChoiceField, True),
        }
        check_create_get(user_client, url, fields_cnt, fields)

    @pytest.mark.django_db(transaction=True)
    def test_create_view_post(self, user_client, user, user_two):
        text = 'Текст отзыва'
        score = 'PV'
        url = f'/profile/{user_two.username}/reviews/create/'
        redirect_url = f'/profile/{user_two.username}/reviews/'
        response = user_client.post(url, data={'text': text, 'score': score})
        created_object = Review.objects.filter(
            author=user, text=text, score=score
        ).first()
        check_create_post(user_client, response, url,
                          redirect_url, created_object)
