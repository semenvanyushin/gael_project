from django.contrib import admin

from chats.models import Chat, Message


@admin.register(Message)
class Message(admin.ModelAdmin):
    list_display = (
        'id',
        'get_chat',
        'get_author',
        'message',
        'pub_date',
        'is_readed',
    )
    search_fields = ('get_chat', 'pub_date')
    list_filter = ('author', 'is_readed', 'pub_date')
    empty_value_display = '-пусто-'

    @admin.display(description='Чат')
    def get_chat(self, obj):
        return obj.chat.type

    @admin.display(description='Автор')
    def get_author(self, obj):
        return obj.author.username


@admin.register(Chat)
class Chat(admin.ModelAdmin):
    list_display = (
        'id',
        'type',
        'get_members',
    )
    search_fields = ('get_members',)
    list_filter = ('type',)
    empty_value_display = '-пусто-'

    @admin.display(description='Участники')
    def get_members(self, obj):
        return '\n '.join([
            f'{item["username"]}, '
            for item in obj.members.values(
                'username')
        ])
