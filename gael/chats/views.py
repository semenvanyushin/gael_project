from django.db.models.aggregates import Count
from django.shortcuts import redirect, render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from django.views import View

from chats.models import Chat
from chats.forms import MessageForm


class DialogsView(LoginRequiredMixin, View):
    def get(self, request):
        chats = Chat.objects.filter(members__in=[request.user.id])
        return render(request,
                      'chats/dialogs.html',
                      {'user_profile': request.user, 'chats': chats})


class CreateDialogView(LoginRequiredMixin, View):
    def get(self, request, user_id):
        chats = Chat.objects.filter(
            members__in=[request.user.id, user_id],
            type=Chat.DIALOG).annotate(c=Count('members')).filter(c=2)
        if chats.count() == 0:
            chat = Chat.objects.create()
            chat.members.add(request.user)
            chat.members.add(user_id)
        else:
            chat = chats.first()
        return redirect(reverse('chats:messages', kwargs={'chat_id': chat.id}))


class MessagesView(LoginRequiredMixin, View):
    def get(self, request, chat_id):
        try:
            chat = Chat.objects.get(id=chat_id)
            if request.user in chat.members.all():
                chat.message_set.filter(
                    is_readed=False).exclude(
                        author=request.user).update(is_readed=True)
            else:
                chat = None
        except Chat.DoesNotExist:
            chat = None

        return render(
            request,
            'chats/messages.html',
            {
                'user_profile': request.user,
                'chat': chat,
                'form': MessageForm()
            }
        )

    def post(self, request, chat_id):
        form = MessageForm(data=request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.chat_id = chat_id
            message.author = request.user
            message.save()
        return redirect(reverse('chats:messages', kwargs={'chat_id': chat_id}))
