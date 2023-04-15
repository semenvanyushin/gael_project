from django import forms

from posts.models import PostSale, Review


class PostSaleForm(forms.ModelForm):

    class Meta:
        model = PostSale
        fields = ['game', 'price', 'type_payment']
        labels = {
            'game': 'Игра',
            'price': 'Цена',
            'type_payment': 'Вариант оплаты',
        }

    def __init__(self, *args, **kwargs):
        super(PostSaleForm, self).__init__(*args, **kwargs)
        self.fields['game'].empty_label = " Выбери игру "


class ReviewForm(forms.ModelForm):

    class Meta:
        model = Review
        fields = ['text', 'score']
        labels = {
            'text': 'Текст отзыва',
            'score': 'Тип отзыва',
        }
