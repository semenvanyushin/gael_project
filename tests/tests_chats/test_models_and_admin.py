import pytest
from django.contrib.auth import get_user_model
from django_ckeditor_5.fields import CKEditor5Field
from django.db.models import fields

from tests.utils import admin_test, check_field


try:
    from chats.models import Chat
except ImportError:
    assert False, 'Не найдена модель Chat'
try:
    from chats.models import Message
except ImportError:
    assert False, 'Не найдена модель Message'


class TestChat:

    def test_chat_model(self):
        model = Chat
        model_fields = Chat._meta.fields
        field_name_and_type = {
            'type': (fields.CharField, 1)
        }
        check_field(model, model_fields, **field_name_and_type)

    @pytest.mark.django_db(transaction=True)
    def test_chat_create(self, user):
        assert Chat.objects.count() == 0
        chat = Chat.objects.create(type='D')
        chat.members.add(user)
        chat.save()
        assert Chat.objects.count() == 1
        assert Chat.objects.get(type='D', members=user).pk == chat.pk

    def test_chat_admin(self):
        model = Chat
        chat_admin_fields = ('type', 'get_members',)
        chat_admin_search_fields = ('get_members',)
        chat_admin_list_filter = ('type',)
        admin_test(model, chat_admin_fields,
                   chat_admin_search_fields,
                   chat_admin_list_filter)


class TestMessage:

    def test_message_model(self):
        model = Message
        model_fields = Message._meta.fields
        field_name_and_type = {
            'message': (CKEditor5Field,),
            'pub_date': (fields.DateTimeField,),
            'chat_id': (fields.related.ForeignKey, Chat),
            'author_id': (fields.related.ForeignKey, get_user_model()),
            'is_readed': (fields.BooleanField,)
        }
        check_field(model, model_fields, **field_name_and_type)

    @pytest.mark.django_db(transaction=True)
    def test_message_create(self, chat, user):
        message = 'Тестовый текст'
        assert Message.objects.count() == 0
        test_message = Message.objects.create(
            chat=chat, author=user, message=message, is_readed=False)
        assert Message.objects.count() == 1
        assert Message.objects.get(
            chat=chat, author=user, message=message, is_readed=False
        ).pk == test_message.pk

    def test_message_admin(self):
        model = Message
        message_admin_fields = ('get_chat', 'get_author', 'message',
                                'pub_date', 'is_readed',)
        message_admin_search_fields = ('get_chat', 'pub_date',)
        message_admin_list_filter = ('author', 'is_readed', 'pub_date',)
        admin_test(model, message_admin_fields,
                   message_admin_search_fields,
                   message_admin_list_filter)
