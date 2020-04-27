from django.urls import path

from . import views

urlpatterns = [
    path('<int:card_id>/flip', views.flip, name='card_flip'),
]
