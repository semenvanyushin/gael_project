from django.contrib import admin

from posts.models import Game, PostSale, Review


@admin.register(Game)
class Game(admin.ModelAdmin):
    list_display = (
        'id',
        'name',
        'organizer',
        'type_activation',
        'store_region'
    )
    search_fields = ('name', 'organizer')
    list_filter = ('name', 'organizer', 'store_region')
    empty_value_display = '-пусто-'


@admin.register(PostSale)
class PostSale(admin.ModelAdmin):
    list_display = (
        'id',
        'author',
        'game',
        'price',
        'type_payment',
        'pub_date'
    )
    search_fields = ('author', 'get_game_name', 'pub_date')
    list_filter = ('author', 'game', 'pub_date')
    empty_value_display = '-пусто-'

    @admin.display(description='Название игры')
    def get_game_name(self, obj):
        return obj.game.name


@admin.register(Review)
class Review(admin.ModelAdmin):
    list_display = (
        'id',
        'user',
        'author',
        'text',
        'score',
        'pub_date'
    )
    search_fields = ('user', 'author', 'score')
    list_filter = ('user', 'author', 'pub_date')
    empty_value_display = '-пусто-'
