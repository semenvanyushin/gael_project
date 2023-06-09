# Generated by Django 4.1.7 on 2023-04-21 22:56

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Account',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('login', models.CharField(max_length=255, verbose_name='Учетная запись игры')),
                ('store_region', models.CharField(max_length=50, verbose_name='Регион магазина')),
                ('logo_region', models.ImageField(blank=True, upload_to='static/logo_region/%Y/%m/%d/', verbose_name='Логотип региона')),
                ('creation_date', models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')),
            ],
            options={
                'verbose_name': 'Учетная запись',
                'verbose_name_plural': 'Учетные записи',
                'ordering': ('-creation_date',),
            },
        ),
        migrations.CreateModel(
            name='Game',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='Название игры')),
                ('logo', models.ImageField(blank=True, upload_to='static/logo/%Y/%m/%d/', verbose_name='Логотип игры')),
                ('description', models.TextField(verbose_name='Описание игры')),
                ('rating', models.FloatField(validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(10)], verbose_name='Рейтинг игры')),
                ('release_date', models.CharField(max_length=50, verbose_name='Дата выхода')),
                ('creation_date', models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')),
            ],
            options={
                'verbose_name': 'Игра',
                'verbose_name_plural': 'Игры',
                'ordering': ('-creation_date',),
            },
        ),
        migrations.CreateModel(
            name='Owner',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('platform', models.CharField(max_length=100, verbose_name='Платформа')),
                ('type_activation', models.CharField(max_length=10, verbose_name='Тип активации')),
                ('creation_date', models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')),
            ],
            options={
                'verbose_name': 'Владелец',
                'verbose_name_plural': 'Владельцы',
                'ordering': ('-creation_date',),
            },
        ),
    ]
