from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

User = get_user_model()


class Owner(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='owner',
        verbose_name='Владелец',
    )
    platform = models.CharField(
        'Платформа',
        max_length=100
    )
    type_activation = models.CharField(
        'Тип активации',
        max_length=10,
    )
    creation_date = models.DateTimeField(
        'Дата создания',
        auto_now_add=True,
    )

    class Meta:
        ordering = ('-creation_date',)
        verbose_name = 'Владелец'
        verbose_name_plural = 'Владельцы'

    def __str__(self):
        return (f'Владелец: {self.user.username} '
                f'Платформа: {self.platform}, Тип: {self.type_activation}')


class Game(models.Model):
    name = models.CharField(
        'Название игры',
        max_length=255,
    )
    logo = models.ImageField(
        'Логотип игры',
        upload_to='static/logo/%Y/%m/%d/',
        blank=True,
    )
    description = models.TextField(
        'Описание игры'
    )
    rating = models.FloatField(
        'Рейтинг игры',
        validators=(
            MinValueValidator(1),
            MaxValueValidator(10)
        )
    )
    release_date = models.CharField(
        'Дата выхода',
        max_length=50
    )
    creation_date = models.DateTimeField(
        'Дата создания',
        auto_now_add=True,
    )

    class Meta:
        ordering = ('-creation_date',)
        verbose_name = 'Игра'
        verbose_name_plural = 'Игры'

    def __str__(self):
        return f'{self.name}'


class Account(models.Model):
    organizer = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name='organizer',
        verbose_name='Организатор',
    )
    game = models.ForeignKey(
        Game,
        on_delete=models.PROTECT,
        related_name='game',
        verbose_name='Игра',
    )
    login = models.CharField(
        'Учетная запись игры',
        max_length=255,
    )
    owners = models.ManyToManyField(
        Owner,
        related_name='owners',
        verbose_name='Владельцы'
    )
    store_region = models.CharField(
        'Регион магазина',
        max_length=50,
    )
    logo_region = models.ImageField(
        'Логотип региона',
        upload_to='static/logo_region/%Y/%m/%d/',
        blank=True,
    )
    creation_date = models.DateTimeField(
        'Дата создания',
        auto_now_add=True,
    )

    class Meta:
        ordering = ('-creation_date',)
        verbose_name = 'Учетная запись'
        verbose_name_plural = 'Учетные записи'
        constraints = [
            models.UniqueConstraint(
                fields=['organizer', 'login'], name='unique_login')]

    def __str__(self):
        return (f'Аккаунт: {self.login}, Регион: {self.store_region} '
                f'Организатор:{self.organizer.username}')
