from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('team_creation/<int:game_id>/', views.team_creation, name='team_creation'),
    path('team_creation/<int:game_id>/<int:team_id>/', views.team_page, name='team_page'),
    path('game_list', views.game_list, name='game_list'),
    path('game_session', views.game_session, name='game_session'),
    path("start_page", views.start_page, name='start_page'),
    path("player_registration_form", views.player_registration_form, name='player_registration_form'),
]