from django.contrib.auth import get_user_model
from django_ckeditor_5.fields import CKEditor5Field
from django.db import models

User = get_user_model()


class Chat(models.Model):
    DIALOG = 'D'
    CHAT = 'C'
    CHAT_TYPE_CHOICES = (
        (DIALOG, 'Диалог'),
        (CHAT, 'Чат')
    )

    type = models.CharField(
        'Тип',
        max_length=1,
        choices=CHAT_TYPE_CHOICES,
        default=DIALOG
    )
    members = models.ManyToManyField(User, verbose_name='Участник')

    class Meta:
        verbose_name = 'Чат'
        verbose_name_plural = 'Чаты'


class Message(models.Model):
    chat = models.ForeignKey(
        Chat,
        verbose_name='Чат',
        on_delete=models.CASCADE)
    author = models.ForeignKey(
        User,
        verbose_name='Пользователь',
        on_delete=models.CASCADE)
    message = CKEditor5Field('Сообщение', config_name='extends')
    pub_date = models.DateTimeField('Дата сообщения', auto_now_add=True)
    is_readed = models.BooleanField('Прочитано', default=False)

    class Meta:
        ordering = ['pub_date']
        verbose_name = 'Сообщение'
        verbose_name_plural = 'Сообщения'

    def __str__(self):
        return self.message
