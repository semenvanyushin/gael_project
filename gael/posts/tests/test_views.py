import shutil
import tempfile

from django import forms
from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import Client, TestCase, override_settings
from django.urls import reverse

from posts.models import Game, PostSale, Review

User = get_user_model()

TEMP_MEDIA_ROOT = tempfile.mkdtemp(dir=settings.BASE_DIR)


@override_settings(MEDIA_ROOT=TEMP_MEDIA_ROOT)
class PostPagesTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.test_user = User.objects.create_user(
            username='another_user',
            email='test@mail.ru',
            first_name='name',
            last_name='surname',
        )
        cls.user_author = User.objects.create_user(
            username='user_author',
            email='test_author@mail.ru',
            first_name='author',
            last_name='surname author',
        )
        small_gif = (
            b'\x47\x49\x46\x38\x39\x61\x02\x00'
            b'\x01\x00\x80\x00\x00\x00\x00\x00'
            b'\xFF\xFF\xFF\x21\xF9\x04\x00\x00'
            b'\x00\x00\x00\x2C\x00\x00\x00\x00'
            b'\x02\x00\x01\x00\x00\x02\x02\x0C'
            b'\x0A\x00\x3B'
        )
        uploaded = SimpleUploadedFile(
            name='small.gif',
            content=small_gif,
            content_type='image/gif'
        )
        cls.game = Game.objects.create(
            owner=cls.test_user,
            name='тестовое название игры',
            login='game1@mail.ru',
            organizer='организатор тест',
            platform='playstation 5',
            type_activation='тестовое тип активации',
            store_region='тестовый регион',
            logo=uploaded,
        )
        cls.post = PostSale.objects.create(
            author=cls.test_user,
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

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        shutil.rmtree(TEMP_MEDIA_ROOT, ignore_errors=True)

    def setUp(self):
        self.authorized_user = Client()
        self.author_user = Client()
        self.authorized_user.force_login(self.test_user)
        self.author_user.force_login(self.user_author)

    def test_pages_uses_correct_template(self):
        """URL-адрес использует соответствующий шаблон."""
        page_template_names = {
            reverse('posts:index'): 'posts/index.html',
            reverse('posts:post_create'): 'posts/create_post.html',
            reverse(
                'posts:post_edit',
                kwargs={'post_id': self.post.id}): 'posts/create_post.html',
            reverse(
                'posts:profile',
                kwargs={
                    'username': self.test_user.username
                }): 'posts/profile.html',
            reverse(
                'posts:review',
                kwargs={
                    'username': self.test_user.username
                }): 'posts/review.html',
            reverse(
                'posts:review_create',
                kwargs={
                    'username': self.author_user
                }): 'posts/review_create.html',
        }

        for reverse_name, template in page_template_names.items():
            with self.subTest(reverse_name=reverse_name):
                response = self.authorized_user.get(reverse_name)
                self.assertTemplateUsed(response, template)

    def check_list_post_context(self, context):
        with self.subTest(context=context):
            self.assertEqual(context.pub_date, self.post.pub_date)
            self.assertEqual(context.author, self.post.author)
            self.assertEqual(context.price, self.post.price)
            self.assertEqual(context.type_payment, self.post.type_payment)
            self.assertEqual(context.game, self.post.game)

    def test_index_page_show_correct_context(self):
        """Шаблон index сформирован с правильным контекстом."""
        response = self.authorized_user.get(reverse('posts:index'))
        self.check_list_post_context(response.context['posts'][0])

    def test_profile_page_show_correct_context(self):
        """Шаблон profile сформирован с правильным контекстом."""
        response = self.authorized_user.get(reverse(
            'posts:profile',
            kwargs={'username': self.test_user.username}
        ))
        self.assertEqual(response.context['author'], self.test_user)
        self.check_list_post_context(response.context['user_posts'][0])

    def check_list_review_context(self, context):
        with self.subTest(context=context):
            self.assertEqual(context.pub_date, self.review.pub_date)
            self.assertEqual(context.author, self.review.author)
            self.assertEqual(context.text, self.review.text)
            self.assertEqual(context.user, self.review.user)
            self.assertEqual(context.score, self.review.score)

    def test_review_page_show_correct_context(self):
        """Шаблон review сформирован с правильным контекстом."""
        response = self.authorized_user.get(reverse(
            'posts:review',
            kwargs={'username': self.test_user.username}))
        self.assertEqual(response.context['author'], self.test_user)
        self.check_list_review_context(response.context['reviews'][0])

    def test_form_post_create_and_edit_show_correct(self):
        """Формы на страницах post_create и post_edit корректны."""
        context = {
            reverse('posts:post_create'),
            reverse('posts:post_edit', kwargs={'post_id': self.post.id})
        }
        for reverse_page in context:
            with self.subTest(reverse_page=reverse_page):
                response = self.authorized_user.get(reverse_page)
                form_field = response.context['form'].fields['game']
                self.assertIsInstance(form_field, forms.fields.ChoiceField)
                form_field = response.context['form'].fields['price']
                self.assertIsInstance(form_field, forms.fields.IntegerField)
                form_field = response.context['form'].fields['type_payment']
                self.assertIsInstance(form_field, forms.fields.CharField)

    def test_form_review_create_show_correct(self):
        """Формы на страницах review_create корректны."""
        context = {
            reverse('posts:review_create',
                    kwargs={'username': self.test_user.username}),
        }
        for reverse_page in context:
            with self.subTest(reverse_page=reverse_page):
                response = self.authorized_user.get(reverse_page)
                form_field = response.context['form'].fields['text']
                self.assertIsInstance(form_field, forms.fields.CharField)
                form_field = response.context['form'].fields['score']
                self.assertIsInstance(form_field, forms.fields.IntegerField)
