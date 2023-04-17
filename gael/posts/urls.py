from django.urls import path
from posts.views import (MarketPage, PostSaleCreate, PostSaleDelete,
                         PostSaleUpdate, ProfilePage, ReviewPage,
                         ReviewCreate, ReviewDelete)

app_name = 'posts'

urlpatterns = [
    path('', MarketPage.as_view(), name='index'),
    path('create/', PostSaleCreate.as_view(), name='post_create'),
    path('posts/<int:post_id>/edit/',
         PostSaleUpdate.as_view(), name='post_edit'),
    path('posts/<int:post_id>/delete/',
         PostSaleDelete.as_view(), name='post_delete'),
    path('profile/<str:username>/', ProfilePage.as_view(), name='profile'),
    path('profile/<str:username>/reviews/create/',
         ReviewCreate.as_view(), name='review_create'),
    path('profile/<str:username>/reviews/',
         ReviewPage.as_view(), name='review'),
    path('profile/<str:username>/reviews/<int:review_id>/',
         ReviewDelete.as_view(), name='review_delete'),
]
