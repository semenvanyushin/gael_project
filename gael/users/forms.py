from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django import forms

from users.models import AdditionsToTheProfile

User = get_user_model()


class CreationForm(UserCreationForm):

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('first_name', 'last_name', 'username', 'email')


class AdditionsToTheProfileForm(forms.ModelForm):

    class Meta:
        model = AdditionsToTheProfile
        fields = ['avatar', 'telegram']
        labels = {
            'avatar': 'Изображение аккаунта',
            'telegram': 'Телеграм',
        }
