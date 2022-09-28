from django.urls import path
from . import views

app_name="app"

urlpatterns = [
    path('chatty', views.index, name='index'),
    path('chatty/<str:room_name>/', views.room, name='room'),
    # AC
    path('team_creation/<int:game_id>/<int:player_id>', views.team_creation, name='team_creation'),
    # AC
    path('team_page/<int:game_id>/<int:team_id>/<int:player_id>', views.team_page, name='team_page'),
    path('player_game_assignation/<int:game_id>', views.player_game_assignation, name='player_game_assignation'),
    path('player_game_assignation/<int:game_id>/<int:player_id>', views.player_game_assignation, name='player_game_assignation'),
    path('game_list', views.game_list, name='game_list'),
    path('game_list/<int:player_id>', views.game_list, name='game_list'),
    path('game_session/<int:game_id>/<int:player_id>', views.game_session, name='game_session'),
    path("", views.start_page, name='start_page'),
    path("host_player_registration_form", views.host_player_registration_form, name='host_player_registration_form'),
    path("join_player_registration_form", views.join_player_registration_form, name='join_player_registration_form'),
    path("question_clue_spectrum/<int:game_id>/<int:team_id>/<int:player_id>", views.question_clue_spectrum, name='question_clue_spectrum'),
    path("clue_form_one", views.clue_form_one, name="clue_form_one"),
    path("clue_form_two", views.clue_form_two, name="clue_form_two"),
    path("game_end", views.game_end, name="game_end"),
    # path("team_score", views.team_score, name='team_score'),
    path("waiting_room/<host>", views.waiting_room, name="waiting_room"),
    path("game_turn/<int:game_id>/<int:team_id>/<int:player_id>", views.game_turn, name="game_turn"),
    path("question_response_form", views.question_response_form, name="question_response_form"),
    path("question_save", views.question_save, name="question_save"),
    path("scale", views.scale, name="scale"),
    path("dashboard", views.dashboard, name="dashboard"),
    path("dashboard/games", views.dashboard_games, name="dashboard_games"),
    path("dashboard/players", views.dashboard_players, name="dashboard_players"),
    path("dashboard/teams", views.dashboard_teams, name="dashboard_teams"),
    path("dashboard/questions", views.dashboard_questions, name="dashboard_questions"),
    path("dashboard/player_clues", views.dashboard_player_clues, name="dashboard_player_clues"),

]