from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.safestring import mark_safe


class User(AbstractUser):
    email = models.EmailField(max_length=255, unique=True,)
    first_name = models.CharField('Имя', max_length=255,)
    last_name = models.CharField('Фамилия', max_length=255,)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    class Meta:
        ordering = ('id',)
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.email


class AdditionsToTheProfile(models.Model):
    user = models.ForeignKey(
        User, verbose_name='Пользователь', on_delete=models.CASCADE)
    avatar = models.ImageField(
        'Avatar', upload_to='static/avatar/%Y/%m/%d/', null=True, blank=True)
    telegram = models.CharField(
        'Телеграм', max_length=255, null=True, blank=True)

    def __str__(self):
        return self.user.username

    def get_avatar(self):
        if not self.avatar:
            return '/static/img/avatar_default.png'
        return self.avatar.url

    def avatar_tag(self):
        return mark_safe(
            '<img src="%s" width="50" height="50" />' % self.get_avatar())

    avatar_tag.short_description = 'Avatar'

    class Meta:
        ordering = ('id',)
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.user.username
