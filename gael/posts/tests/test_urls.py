from collections import namedtuple
from http import HTTPStatus

from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse

from posts.models import Game, PostSale, Review

User = get_user_model()


class StaticURLTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user_author = User.objects.create_user(
            username='user_author',
            email='test_author@mail.ru',
            first_name='author',
            last_name='surname author',
        )
        cls.test_user = User.objects.create_user(
            username='another_user',
            email='test@mail.ru',
            first_name='name',
            last_name='surname',
        )
        cls.game = Game.objects.create(
            owner=cls.user_author,
            name='тестовое название игры',
            login='game1@mail.ru',
            organizer='организатор тест',
            platform='playstation 5',
            type_activation='тестовое тип активации',
            store_region='тестовый регион',
        )
        cls.post = PostSale.objects.create(
            author=cls.user_author,
            game=cls.game,
            price=500,
            type_payment='вариант оплаты',
        )
        cls.review = Review.objects.create(
            user=cls.test_user,
            text='Тестовый текст отзыва',
            author=cls.user_author,
            score=1,
        )
        check_info = namedtuple(
            'check_info',
            ('template, guest_exist_code, '
             'authtorized_exist_code, author_exist_code')
        )
        cls.no_template = (
            '/unexisting_page/',
            reverse('posts:post_delete', kwargs={'post_id': cls.post.id}),
            reverse('posts:review_delete',
                    kwargs={'username': cls.test_user.username,
                            'review_id': cls.review.id})
        )
        cls.values_for_url = {
            reverse('posts:index'): check_info(
                'posts/index.html',
                HTTPStatus.FOUND,
                HTTPStatus.OK,
                HTTPStatus.OK,
            ),
            '/unexisting_page/': check_info(
                AssertionError,
                HTTPStatus.NOT_FOUND,
                HTTPStatus.NOT_FOUND,
                HTTPStatus.NOT_FOUND,
            ),
            reverse('posts:post_edit',
                    kwargs={'post_id': cls.post.id}): check_info(
                'posts/create_post.html',
                HTTPStatus.FOUND,
                HTTPStatus.FOUND,
                HTTPStatus.OK,
            ),
            reverse('posts:post_create'): check_info(
                'posts/create_post.html',
                HTTPStatus.FOUND,
                HTTPStatus.OK,
                HTTPStatus.OK,
            ),
            reverse('posts:post_delete',
                    kwargs={'post_id': cls.post.id}): check_info(
                AssertionError,
                HTTPStatus.FOUND,
                HTTPStatus.FOUND,
                HTTPStatus.FOUND,
            ),
            reverse('posts:profile',
                    kwargs={'username': cls.test_user.username}): check_info(
                'posts/profile.html',
                HTTPStatus.FOUND,
                HTTPStatus.OK,
                HTTPStatus.OK,
            ),
            reverse('posts:review_create',
                    kwargs={'username': cls.test_user.username}): check_info(
                'posts/review_create.html',
                HTTPStatus.FOUND,
                HTTPStatus.OK,
                HTTPStatus.OK,
            ),
            reverse('posts:review',
                    kwargs={'username': cls.test_user.username}): check_info(
                'posts/review.html',
                HTTPStatus.FOUND,
                HTTPStatus.OK,
                HTTPStatus.OK,
            ),
            reverse('posts:review_delete',
                    kwargs={'username': cls.test_user.username,
                            'review_id': cls.review.id}): check_info(
                AssertionError,
                HTTPStatus.FOUND,
                HTTPStatus.FOUND,
                HTTPStatus.FOUND,
            ),
        }

    def setUp(self):
        self.guest_client = Client()
        self.post_author = Client()
        self.post_author.force_login(self.user_author)
        self.authorized_user = Client()
        self.authorized_user.force_login(self.test_user)

    def test_urls_uses_correct_template(self):
        """URL-адрес соответствует заданному шаблону."""
        for address, check_info in self.values_for_url.items():
            if address not in self.no_template:
                with self.subTest(adress=address):
                    response = self.post_author.get(address)
                    self.assertTemplateUsed(response, check_info.template)

    def test_urls_exist_guest_user(self):
        """Доступ к страницам. Неавторизованный пользователь."""
        for url, check_info in self.values_for_url.items():
            with self.subTest(url=url):
                response = self.guest_client.get(url).status_code
                self.assertEqual(check_info.guest_exist_code, response)

    def test_urls_exist_authorized_user(self):
        """Доступ к страницам. Авторизованный пользователь."""
        for url, check_info in self.values_for_url.items():
            with self.subTest(url=url):
                response = self.authorized_user.get(url).status_code
                self.assertEqual(check_info.authtorized_exist_code, response)

    def test_urls_exist_post_author(self):
        """Доступ к страницам. Авторизованный пользователь, автор поста."""
        for url, check_info in self.values_for_url.items():
            with self.subTest(url=url):
                response = self.post_author.get(url).status_code
                self.assertEqual(check_info.author_exist_code, response)
