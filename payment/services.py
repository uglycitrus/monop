from deck.models import Card
from turn.services import end_move
from .models import Payment


def assign_victim(payment_id, victim_id, user_id):
    Payment.objects.filter(
        id=payment_id,
        move__turn__user_id=user_id,
        victim=None).update(victim_id=victim_id)


def pay(payment, card, user_id):
    # TODO: handle race
    if payment.is_paid():
        raise Exception('all squared away')
    else:
        payment.received.add(card)
        Card.objects.filter(
            id=card.id,
            user_table_id=user_id).update(
            user_table_id=payment.move.turn.user_id)
        end_move(payment.move)
