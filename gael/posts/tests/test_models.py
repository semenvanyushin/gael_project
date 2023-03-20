from django.contrib.auth import get_user_model
from django.test import TestCase

from posts.models import Game, PostSale, Review

User = get_user_model()


class PostSaleModelTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.test_user = User.objects.create_user(
            username='test_user',
            email='test@mail.ru',
            first_name='name',
            last_name='surname',
        )
        cls.test_author = User.objects.create_user(
            username='test_author',
            email='test_author@mail.ru',
            first_name='author',
            last_name='surname author',
        )
        cls.game = Game.objects.create(
            owner=cls.test_author,
            name='тестовое название игры',
            login='game1@mail.ru',
            organizer='организатор тест',
            platform='playstation 5',
            type_activation='тестовое тип активации',
            store_region='тестовый регион',
        )
        cls.post = PostSale.objects.create(
            author=cls.test_author,
            game=cls.game,
            price=500,
            type_payment='вариант оплаты',
        )
        cls.review = Review.objects.create(
            user=cls.test_user,
            text='Тестовый текст отзыва',
            author=cls.test_author,
            score=1,
        )

    def test_models_have_correct_object_names_post(self):
        """Проверяем, что у модели PostSale корректно работает __str__."""
        post_sale = PostSaleModelTest.post
        expected_object_name = (f'{post_sale.author.username}: '
                                f'{post_sale.game} - {post_sale.price}')
        self.assertEqual(expected_object_name, str(post_sale))

    def test_models_have_correct_object_names_game(self):
        """Проверяем, что у модели Game корректно работает __str__."""
        game = PostSaleModelTest.game
        expected_object_name = f'{game.name}, {game.organizer}'
        self.assertEqual(expected_object_name, str(game))

    def test_models_have_correct_object_names_review(self):
        """Проверяем, что у модели Review корректно работает __str__."""
        review = PostSaleModelTest.review
        expected_object_name = (f'{review.user} написал: '
                                f'{review.author} {review.text}')
        self.assertEqual(expected_object_name, str(review))
