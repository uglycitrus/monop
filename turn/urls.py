from django.urls import path

from . import views

urlpatterns = [
    path('<int:turn_id>/<int:card_id>', views.play, name='play'),
    path('<int:turn_id>/end', views.end, name='end_turn'),
]
