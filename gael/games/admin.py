from django.contrib import admin

from games.models import Account, Game, Owner


@admin.register(Account)
class Account(admin.ModelAdmin):
    list_display = (
        'id',
        'get_organizer_username',
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


@admin.register(Owner)
class Owner(admin.ModelAdmin):
    list_display = (
        'id',
        'get_username',
        'account',
        'platform',
        'type_activation',
        'creation_date',
    )
    search_fields = ('get_username', 'account')
    list_filter = ('creation_date',)
    empty_value_display = '-пусто-'

    @admin.display(description='Владелец')
    def get_username(self, obj):
        return obj.user.username


@admin.register(Game)
class Game(admin.ModelAdmin):
    list_display = (
        'id',
        'owner',
        'name',
        'description',
        'rating',
        'release_date',
        'creation_date',
    )
    search_fields = ('owner', 'name', 'creation_date')
    list_filter = ('owner', 'name', 'creation_date')
    empty_value_display = '-пусто-'
