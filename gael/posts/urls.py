from django.urls import path
from posts.views import (index, post_create, post_delete, post_edit, profile,
                         review, review_create, review_delete)

app_name = 'posts'

urlpatterns = [
    path('', index, name='index'),
    path('create/', post_create, name='post_create'),
    path('posts/<int:post_id>/edit/', post_edit, name='post_edit'),
    path('posts/<int:post_id>/delete/', post_delete, name='post_delete'),
    path('profile/<str:username>/', profile, name='profile'),
    path('profile/<str:username>/reviews/create/',
         review_create, name='review_create'),
    path('profile/<str:username>/reviews/',
         review, name='review'),
    path('profile/<str:username>/reviews/<int:review_id>/',
         review_delete, name='review_delete'),
]
