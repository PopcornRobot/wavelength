from django.urls import path
from . import views

app_name="app"

urlpatterns = [
    path('chatty', views.index, name='index'),
    path('chatty/<str:room_name>/', views.room, name='room'),
    # AC
    path('team_creation/<int:game_id>/', views.team_creation, name='team_creation'),
    # AC
    path('team_page/<int:game_id>/', views.team_page, name='team_page'),    
    
    path('game_list', views.game_list, name='game_list'),
    path('game_session/<int:current_game>', views.game_session, name='game_session'),
    path("start_page", views.start_page, name='start_page'),
    path("host_player_registration_form", views.host_player_registration_form, name='host_player_registration_form'),
    path("join_player_registration_form", views.join_player_registration_form, name='join_player_registration_form'),
    path("question_clue_spectrum", views.question_clue_spectrum, name='question_clue_spectrum'),
    path("clue_form", views.clue_form , name="clue_form"),
    path("game_end", views.game_end, name="game_end"),
    path("team_score", views.team_score, name='team_score'),
    path("waiting_room/<host>", views.waiting_room, name="waiting_room"),
    path("player_game_assignment", views.player_game_assignment, name="player_game_assignment"),
    
]