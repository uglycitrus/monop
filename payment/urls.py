from django.urls import path

from . import views

urlpatterns = [
    path(
        '<int:payment_id>/victim/<int:victim_id>',
        views.assign_victim,
        name='assign_victim'),
    path(
        '<int:payment_id>/pay/<int:card_id>',
        views.pay,
        name='pay'),
]
