from django import forms

from games.models import Account
from posts.models import PostSale, Review


class PostSaleForm(forms.ModelForm):

    class Meta:
        model = PostSale
        fields = ['account', 'price', 'type_payment']
        labels = {
            'account': 'Аккаунт',
            'price': 'Цена',
            'type_payment': 'Вариант оплаты',
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(PostSaleForm, self).__init__(*args, **kwargs)
        self.fields['account'] = forms.ModelChoiceField(
            queryset=Account.objects.select_related(
                'organizer').filter(owners__user=user))
        self.fields['account'].empty_label = " Выбери учетную запись "


class ReviewForm(forms.ModelForm):

    class Meta:
        model = Review
        fields = ['text', 'score']
        labels = {
            'text': 'Текст отзыва',
            'score': 'Тип отзыва',
        }
