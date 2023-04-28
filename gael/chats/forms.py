from django.forms import ModelForm

from chats.models import Message


class MessageForm(ModelForm):
    class Meta:
        model = Message
        fields = ['message']

    def __init__(self, *args, **kwargs):
        '''Обновление стилей формы под Bootstrap'''
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update(
                {'class': 'form-control', 'autocomplete': 'off'})

        self.fields['message'].widget.attrs.update(
            {'class': 'form-control django_ckeditor_5'})
        self.fields['message'].required = False
