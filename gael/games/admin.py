from django.contrib import admin

from games.models import Account, Game, Owner


@admin.register(Account)
class Account(admin.ModelAdmin):
    list_display = (
        'id',
        'get_organizer_username',
        'get_owners',
        'get_game_name',
        'login',
        'store_region',
        'creation_date',
    )
    search_fields = ('login',)
    list_filter = ('store_region', 'creation_date')
    empty_value_display = '-пусто-'

    @admin.display(description='Организатор')
    def get_organizer_username(self, obj):
        return obj.organizer.username

    @admin.display(description='Игра')
    def get_game_name(self, obj):
        return obj.game.name

    @admin.display(description='Владельцы')
    def get_owners(self, obj):
        return '\n '.join([
            f'{item["type_activation"]}, '
            f'{item["user__username"]}, {item["platform"]},'
            for item in obj.owners.values('user__username', 'platform',
                                          'type_activation')
        ])


@admin.register(Owner)
class Owner(admin.ModelAdmin):
    list_display = (
        'id',
        'get_username',
        'platform',
        'type_activation',
        'creation_date',
    )
    search_fields = ('get_username',)
    list_filter = ('creation_date',)
    empty_value_display = '-пусто-'

    @admin.display(description='Владелец')
    def get_username(self, obj):
        return obj.user.username


@admin.register(Game)
class Game(admin.ModelAdmin):
    list_display = (
        'id',
        'name',
        'description',
        'rating',
        'release_date',
        'creation_date',
    )
    search_fields = ('name', 'creation_date')
    list_filter = ('name', 'creation_date')
    empty_value_display = '-пусто-'
