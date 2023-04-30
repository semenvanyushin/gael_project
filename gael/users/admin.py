from django.contrib import admin

from users.models import User, AdditionsToTheProfile


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'email', 'first_name',
                    'last_name', 'date_joined',)
    search_fields = ('email', 'username', 'first_name', 'last_name',)
    list_filter = ('date_joined', 'email', 'first_name',)
    empty_value_display = '-пусто-'


@admin.register(AdditionsToTheProfile)
class AdditionsToTheProfileAdmin(admin.ModelAdmin):
    list_display = ('id', 'avatar_tag', 'user',)
    search_fields = ('user',)
    readonly_fields = ['avatar_tag']
    empty_value_display = '-пусто-'
