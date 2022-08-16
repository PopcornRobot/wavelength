from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path("start_page", views.start_page, name='start_page'),
    path("player_registration_form", views.player_registration_form, name='player_registration_form'),
]