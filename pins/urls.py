from django.urls import path
from .views import (
    pin_list, pin_detail, add_comment, add_like, save_pin, create_pin, login_view, register_view,
    logout_view, create_board, search_pins, user_profile, change_password, user_pins_boards,
    user_likes_saves, board_detail, edit_pin, delete_pin, edit_board, delete_board,
    profile, follow_user, unfollow_user, remove_follower, followers_list, following_list
)

urlpatterns = [
    path('', pin_list, name='pin_list'),
    path('pins/<int:pk>/', pin_detail, name='pin_detail'),
    path('pins/<int:pk>/comment/', add_comment, name='add_comment'),
    path('pins/<int:pk>/like/', add_like, name='add_like'),
    path('pins/<int:pk>/save/', save_pin, name='save_pin'),
    path('pins/<int:pk>/edit/', edit_pin, name='edit_pin'),
    path('pins/<int:pk>/delete/', delete_pin, name='delete_pin'),
    path('pins/create/', create_pin, name='create_pin'),
    path('login/', login_view, name='login'),
    path('register/', register_view, name='register'),
    path('logout/', logout_view, name='logout'),
    path('boards/create/', create_board, name='create_board'),
    path('boards/<int:pk>/', board_detail, name='board_detail'),
    path('boards/<int:pk>/edit/', edit_board, name='edit_board'),
    path('boards/<int:pk>/delete/', delete_board, name='delete_board'),
    path('search/', search_pins, name='search_pins'),
    path('profile/', user_profile, name='user_profile'),
    path('profile/password/', change_password, name='change_password'),
    path('profile/pins-boards/', user_pins_boards, name='user_pins_boards'),
    path('profile/likes-saves/', user_likes_saves, name='user_likes_saves'),
    path('profile/<str:username>/', profile, name='profile'),
    path('profile/<str:username>/follow/', follow_user, name='follow_user'),
    path('profile/<str:username>/unfollow/', unfollow_user, name='unfollow_user'),
    path('profile/<str:username>/remove/', remove_follower, name='remove_follower'),
    path('profile/<str:username>/followers/', followers_list, name='followers_list'),
    path('profile/<str:username>/following/', following_list, name='following_list'),
]