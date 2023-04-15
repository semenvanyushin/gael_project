from django.contrib.auth import get_user_model
from django.db import models

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
        related_name='user',
        verbose_name='Пользователь'
    )
    text = models.TextField('Текст отзыва')
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='author',
        verbose_name='Автор отзыва'
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

    def __str__(self):
        return f'{self.author} написал: {self.user} {self.text}'
