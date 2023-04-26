import pytest

from tests.utils import check_delete_review


class TestReviewView:

    @pytest.mark.django_db(transaction=True)
    def test_review_delete_view_author_post(self, user, user_client, user_two):
        '''Проверяет может ли автор удалить свой пост.'''
        client = user_client
        finish_objects_count = 0
        check_delete_review(user, user_two, client, finish_objects_count)

    @pytest.mark.django_db(transaction=True)
    def test_review_delete_view_not_author_post(self, user,
                                                user_two_client, user_two):
        '''Проверяет может ли другой пользователь удалить пост автора.'''
        client = user_two_client
        finish_objects_count = 1
        check_delete_review(user, user_two, client, finish_objects_count)
