from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

User = get_user_model()


class Game(models.Model):
    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='owner',
        verbose_name='владелец',
    )
    name = models.CharField(
        'Название игры',
        max_length=150,
    )
    login = models.CharField(
        'Учетная запись игры',
        max_length=150,
    )
    organizer = models.CharField(
        'Организатор',
        max_length=100,
    )
    platform = models.CharField(
        'Платформа',
        max_length=50
    )
    type_activation = models.CharField(
        'Тип активации',
        max_length=10,
    )
    store_region = models.CharField(
        'Регион магазина',
        max_length=50,
    )
    logo = models.ImageField(
        'Логотип игры',
        upload_to='static/posts/',
        blank=True
    )

    class Meta:
        ordering = ('name',)
        verbose_name = 'Игра'
        verbose_name_plural = 'Игры'

    def __str__(self):
        return f'{self.name}, {self.organizer}'


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
        max_length=100
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

    class Meta:
        verbose_name = 'Избранный пост'
        verbose_name_plural = 'Избранные посты'

    def __str__(self):
        favorite = [item['name'] for item in self.post_sale.values('game')]
        return f'{self.user} добавил {favorite} в избранное.'


class Review(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='user',
        verbose_name='Пользователь'
    )
    text = models.TextField('Текст отзыва')
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='author',
        verbose_name='Автор отзыва'
    )
    score = models.IntegerField(
        'Оценка',
        validators=(
            MinValueValidator(-1),
            MaxValueValidator(1)
        )
    )
    pub_date = models.DateTimeField(
        'Дата публикации',
        auto_now_add=True,
        db_index=True
    )

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        ordering = ('pub_date',)

    def __str__(self):
        return f'{self.user} написал: {self.author} {self.text}'
