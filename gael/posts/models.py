from django.contrib.auth import get_user_model
from django.db import models
from django.urls import reverse

from games.models import Game

User = get_user_model()


class PostSale(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='posts',
        verbose_name='автор',
    )
    game = models.ForeignKey(
        Game,
        on_delete=models.CASCADE,
        related_name='game',
        verbose_name='игра',
    )
    price = models.IntegerField('Цена')
    type_payment = models.CharField(
        'Вариант оплаты',
        max_length=255
    )
    pub_date = models.DateTimeField(
        'Дата публикации',
        auto_now_add=True,
    )

    class Meta:
        ordering = ('-pub_date',)
        verbose_name = 'Пост о продаже'
        verbose_name_plural = 'Посты о продаже'

    def get_absolute_url(self):
        return reverse(
            'posts:profile', kwargs={'username': self.author.username})

    def __str__(self):
        return f'{self.author.username}: {self.game} - {self.price}'


class FavoritePost(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=True,
        related_name='favorite_post',
        verbose_name='Пользователь')
    post_sale = models.ManyToManyField(
        PostSale,
        related_name='favorite_post',
        verbose_name='Избранный пост')
    creation_date = models.DateTimeField(
        'Дата добавления',
        auto_now_add=True,
    )

    class Meta:
        ordering = ('-creation_date',)
        verbose_name = 'Избранный пост'
        verbose_name_plural = 'Избранные посты'

    def __str__(self):
        favorite = [item['game'] for item in self.post_sale.values('game')]
        return f'{self.user.username} добавил {favorite} в избранное.'


class Review(models.Model):
    NEUTRAL = 'NT'
    POSITIVE = 'PV'
    NEGATIVE = 'NV'
    SCORE_CHOICES = (
        (POSITIVE, 'Положительный'),
        (NEUTRAL, 'Нейтральный'),
        (NEGATIVE, 'Отрицательный'),
    )

    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='author_review',
        verbose_name='Автор отзыва'
    )
    text = models.TextField('Текст отзыва')
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='user_review',
        verbose_name='Объект отзыва'
    )
    score = models.CharField(
        'оценка',
        max_length=2,
        choices=SCORE_CHOICES,
        default=POSITIVE,
    )
    pub_date = models.DateTimeField(
        'Дата публикации',
        auto_now_add=True,
        db_index=True
    )

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        ordering = ('-pub_date',)

    def get_absolute_url(self):
        return reverse(
            'posts:review', kwargs={'username': self.user.username})

    def __str__(self):
        return (f'{self.author.username} написал '
                f'про {self.user.username}: {self.text}')
