# Generated by Django 4.1.7 on 2023-04-26 17:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chats', '0002_alter_chat_options_alter_message_options'),
    ]

    operations = [
        migrations.AlterField(
            model_name='message',
            name='pub_date',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Дата сообщения'),
        ),
    ]
