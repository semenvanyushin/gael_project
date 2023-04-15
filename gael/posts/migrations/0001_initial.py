# Generated by Django 4.1.7 on 2023-03-22 11:37

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('games', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField(verbose_name='Текст отзыва')),
                ('score', models.IntegerField(validators=[django.core.validators.MinValueValidator(-1), django.core.validators.MaxValueValidator(1)], verbose_name='Оценка')),
                ('pub_date', models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='Дата публикации')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user', to=settings.AUTH_USER_MODEL, verbose_name='Пользователь')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='author', to=settings.AUTH_USER_MODEL, verbose_name='Автор отзыва')),
            ],
            options={
                'verbose_name': 'Отзыв',
                'verbose_name_plural': 'Отзывы',
                'ordering': ('-pub_date',),
            },
        ),
        migrations.CreateModel(
            name='PostSale',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price', models.IntegerField(verbose_name='Цена')),
                ('type_payment', models.CharField(max_length=100, verbose_name='Вариант оплаты')),
                ('pub_date', models.DateTimeField(auto_now_add=True, verbose_name='Дата публикации')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='posts', to=settings.AUTH_USER_MODEL, verbose_name='автор')),
                ('game', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='game', to='games.game', verbose_name='игра')),
            ],
            options={
                'verbose_name': 'Пост о продаже',
                'verbose_name_plural': 'Посты о продаже',
                'ordering': ('-pub_date',),
            },
        ),
        migrations.CreateModel(
            name='FavoritePost',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('creation_date', models.DateTimeField(auto_now_add=True, verbose_name='Дата покупки')),
                ('post_sale', models.ManyToManyField(related_name='favorite_post', to='posts.postsale', verbose_name='Избранный пост')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='favorite_post', to=settings.AUTH_USER_MODEL, verbose_name='Пользователь')),
            ],
            options={
                'verbose_name': 'Избранный пост',
                'verbose_name_plural': 'Избранные посты',
                'ordering': ('-creation_date',),
            },
        ),
    ]
