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


class ReviewForm(forms.ModelForm):

    class Meta:
        model = Review
        fields = ['text', 'score']
        labels = {
            'text': 'Текст отзыва',
            'score': 'Оценка',
        }
        help_texts = {
            'score': 'Варианты: 1, 0 или -1'
        }
