from django.urls import reverse_lazy
import pytest

from posts.models import Review


class TestReviewView:

    @pytest.mark.django_db(transaction=True)
    def test_review_delete_view_author_get(self, user, user_client, user_two):
        assert Review.objects.count() == 0
        review_for_delete = Review.objects.create(
            author=user, user=user_two, score='PV', text='текст отзыва'
        )
        assert Review.objects.count() == 1, (
            'Проверьте модель `Review`, не удается создать пост.'
        )
        url = reverse_lazy(
            'posts:review_delete',
            kwargs={'username': user_two.username,
                    'review_id': review_for_delete.id}
        )
        user_client.post(url)
        assert Review.objects.count() == 0, (
            'Проверьте, что автор поста может удалить свой пост.'
        )

    @pytest.mark.django_db(transaction=True)
    def test_review_delete_view_not_author_post(self, user,
                                                user_two_client, user_two):
        assert Review.objects.count() == 0
        review_for_delete = Review.objects.create(
            author=user, user=user_two, score='PV', text='текст отзыва'
        )
        assert Review.objects.count() == 1, (
            'Проверьте модель `Review`, не удается создать пост.'
        )
        url = reverse_lazy(
            'posts:review_delete',
            kwargs={'username': user_two.username,
                    'review_id': review_for_delete.id}
        )
        response = user_two_client.post(url)
        assert response.status_code in (301, 302), (
            f'Проверьте, что со страницы `{url}` перенаправляете на страницу '
            'пользователя, если запрос не от автора поста'
        )
        assert Review.objects.count() == 1, (
            'Проверьте, что только автор поста может удалить свой пост.'
        )
