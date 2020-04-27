from django.urls import path

from . import views

urlpatterns = [
    path('list', views.list, name='game_list'),
    path('<int:game_id>/', views.detail, name='game_detail'),
    path('<int:game_id>/start-turn', views.start_turn, name='start-turn'),
]
