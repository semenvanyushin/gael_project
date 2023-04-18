from django.contrib import admin

from posts.models import FavoritePost, PostSale, Review


@admin.register(PostSale)
class PostSale(admin.ModelAdmin):
    list_display = (
        'id',
        'get_username',
        'game',
        'price',
        'type_payment',
        'pub_date'
    )
    search_fields = ('get_game_name', 'pub_date')
    list_filter = ('game', 'pub_date')
    empty_value_display = '-пусто-'

    @admin.display(description='Название игры')
    def get_game_name(self, obj):
        return obj.game.name

    @admin.display(description='Автор')
    def get_username(self, obj):
        return obj.author.username


@admin.register(Review)
class Review(admin.ModelAdmin):
    list_display = (
        'id',
        'get_author_username',
        'get_user_username',
        'text',
        'score',
        'pub_date'
    )
    search_fields = ('user', 'author', 'score')
    list_filter = ('user', 'author', 'pub_date')
    empty_value_display = '-пусто-'

    @admin.display(description='Автор')
    def get_author_username(self, obj):
        return obj.author.username

    @admin.display(description='Пользователь')
    def get_user_username(self, obj):
        return obj.user.username


@admin.register(FavoritePost)
class FavoritePost(admin.ModelAdmin):
    list_display = (
        'id',
        'get_username',
        'get_post_sale',
        'creation_date',
    )
    search_fields = ('get_post_sale',)
    list_filter = ('creation_date',)
    empty_value_display = '-пусто-'

    @admin.display(description='Пост о продаже')
    def get_post_sale(self, obj):
        return '\n '.join([
            f'Автор: {item["author__username"]}, Игра: {item["game__name"]}, '
            f'Цена: {item["price"]} руб.'
            for item in obj.post_sale.values(
                'author__username', 'game__name', 'price')
        ])

    @admin.display(description='Пользователь')
    def get_username(self, obj):
        return obj.user.username
