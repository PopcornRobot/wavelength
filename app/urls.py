from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('game_registration/<int:game_id>', views.game_registration, name='game_registration'),
    path('team_creation/<int:game_id>/<int:player_id>', views.team_creation, name='team_creation'),
    path('game_room/<int:player_id>', views.game_room, name='game_room'),
    path('game_list', views.game_list, name='game_list'),
    path('game_session', views.game_session, name='game_session'),
    path("start_page", views.start_page, name='start_page'),
    path("player_registration_form", views.player_registration_form, name='player_registration_form'),
]