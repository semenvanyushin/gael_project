from django.urls import path

from chats.views import CreateDialogView, DialogsView, MessagesView

app_name = 'chats'

urlpatterns = [
    path('', DialogsView.as_view(), name='dialogs'),
    path('create/<int:user_id>/',
         (CreateDialogView.as_view()), name='create_dialog'),
    path('<int:chat_id>/', (MessagesView.as_view()), name='messages'),
]
