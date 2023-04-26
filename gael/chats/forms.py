from django.forms import ModelForm

from chats.models import Message


class MessageForm(ModelForm):
    class Meta:
        model = Message
        fields = ['message']
        labels = {'message': ""}
