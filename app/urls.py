from django.urls import path
from . import views

app_name="app"

urlpatterns = [
    path("", views.start_page, name="start_page"),
    path("host", views.host_start_page, name="host_start_page"),
    path("chatty", views.index, name="index"),
    path("chatty/<str:room_name>/", views.room, name="room"),
    path("cleaning_data_base/<int:game_id>", views.cleaning_data_base, name="cleaning_data_base"),
    path("clue_form", views.clue_form, name="clue_form"),
    path("dashboard", views.dashboard, name="dashboard"),
    path("dashboard/games", views.dashboard_games, name="dashboard_games"),
    path("dashboard/players", views.dashboard_players, name="dashboard_players"),
    path("dashboard/teams", views.dashboard_teams, name="dashboard_teams"),
    path("dashboard/questions", views.dashboard_questions, name="dashboard_questions"),
    path("dashboard/player_clues", views.dashboard_player_clues, name="dashboard_player_clues"),
    path("game_end/<int:game_id>", views.game_end, name="game_end"),
    path("game_list", views.game_list, name="game_list"),
    path("game_list/<int:player_id>", views.game_list, name="game_list"),
    path("game_session/<int:game_id>/<int:player_id>", views.game_session, name="game_session"),
    path("game_turn/<int:game_id>/<int:team_id>/<int:player_id>", views.game_turn, name="game_turn"),
    path("game_result/<int:game_id>/<int:team_id>/<int:player_id>/<int:turn_id>", views.game_result, name="game_result"),
    path("host_player_registration_form", views.host_player_registration_form, name="host_player_registration_form"),
    path("join_player_registration_form", views.join_player_registration_form, name="join_player_registration_form"),
    path("leaving_user/<int:player_id>", views.leaving_user, name="leaving_user"),
    path("player_game_assignation/<int:game_id>", views.player_game_assignation, name="player_game_assignation"),
    path("player_game_assignation/<int:game_id>/<int:player_id>", views.player_game_assignation, name="player_game_assignation"),
    path("question_clue_spectrum/<int:game_id>/<int:team_id>/<int:player_id>", views.question_clue_spectrum, name="question_clue_spectrum"),
    path("scale", views.scale, name="scale"),
    path("team_creation/<int:game_id>/<int:player_id>", views.team_creation, name="team_creation"),
    path("team_page/<int:game_id>/<int:team_id>/<int:player_id>", views.team_page, name="team_page"),
    path("team_answer_response_form/<int:game_id>/<int:team_id>/<int:player_id>/<int:turn_id>", views.team_answer_response_form, name="team_answer_response_form"),
    path("waiting_room/<int:game_id>", views.waiting_room, name="waiting_room"),
    path('game_tutorial', views.game_tutorial, name="game_tutorial"),
]