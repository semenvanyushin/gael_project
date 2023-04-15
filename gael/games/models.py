from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

User = get_user_model()


class Account(models.Model):
    organizer = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='organizer',
        verbose_name='Организатор',
    )
    login = models.CharField(
        'Учетная запись игры',
        max_length=255,
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
        return f'{self.login} ({self.organizer.username})'


class Owner(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='owner',
        verbose_name='Владелец',
    )
    account = models.ForeignKey(
        Account,
        on_delete=models.CASCADE,
        related_name='account',
        verbose_name='Учетная запись',
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
        return f'{self.user.username}'


class Game(models.Model):
    owner = models.ForeignKey(
        Owner,
        on_delete=models.CASCADE,
        blank=True,
        related_name='owner',
        verbose_name='Владелец',
    )
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
        return f'{self.name}, {self.rating}'
