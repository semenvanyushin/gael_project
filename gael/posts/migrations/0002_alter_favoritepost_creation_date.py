# Generated by Django 4.1.7 on 2023-03-22 19:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='favoritepost',
            name='creation_date',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Дата добавления'),
        ),
    ]