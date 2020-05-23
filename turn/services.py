from deck.services import place, play, draw, max_rent
from payment.models import Payment
from .models import Turn, Move, SlyDeal, ForcedDeal, DealBreaker


def _validate_move(turn, index, card, user_id, as_cash=False):
    if index >= 3:
        # inclusive b/c if this is move #3 it's not in the DB yet
        raise Exception('only 3 moves per turn')
    if not (turn.user_id == card.user_hand_id == user_id):
        raise Exception('permission denied')
    if turn.moves.filter(is_active=True).exists():
        raise Exception('previous move hasn\'t completed')
    if card.is_double_rent and not as_cash:
        try:
            previous_move = Move.objects.get(
                turn=turn,
                card__card_type='rent',
                index=index - 1)
        except Move.DoesNotExist:
            raise Exception('you can only play this w/ rent')


def move(turn, card, user_id, as_cash=False):
    index = turn.moves.count()
    _validate_move(turn, index, card, user_id, as_cash=as_cash)
    move = Move.objects.create(
        turn=turn,
        card=card,
        index=index,
        is_active=None if as_cash else card.is_move_active or None)

    if as_cash or card.is_for_placing:
        place(card.id, user_id)
    else:
        play(card.id, user_id)
        _action_mapper(move, card, turn, user_id)
    return move

def _action_mapper(move, card, turn, user_id):
    if card.is_sly_deal:
        SlyDeal.objects.create(move=move)
    elif card.is_forced_deal:
        ForcedDeal.objects.create(move=move)
    elif card.is_deal_breaker:
        DealBreaker.objects.create(move=move)
    elif card.is_payment_generating:
        others = turn.game.users.exclude(id=user_id)
        users = [None, ] if card.victim_limit == 1 else others
        amount = card.victim_amount or max_rent(user_id, turn.game_id, card)
        if not amount:
            raise Exception('You cannot get money with that')
        for u in users:
            Payment.objects.create(move=move, victim=u, amount=amount)
    elif card.is_pass_go:
        draw(turn.game_id, user_id, pass_go=True)
    else:
        raise Exception('what the hell card was that?')
# TODO: 'Hotel', 'House'


def end_move(move):
    Move.objects.filter(id=move.id, is_active=True).update(is_active=None)
    return end_turn(move.turn, None)

def end_turn(turn, user_id):
    if not user_id:
        if turn.moves.count() < 3:
            return turn
        active_move = turn.moves.filter(is_active=True).first()
        if active_move:
            if active_move.is_complete():
                return turn
            else:
                Move.objects.filter(
                    id=active_move.id, is_active=True).update(is_active=None)
    kwargs = {
        'id': turn.id,
        'is_active': True,
    }
    if user_id:
        kwargs['user_id'] = user_id
    return Turn.objects.filter(**kwargs).update(is_active=None)


def pick(move, card, user_id):
    fd = move.forceddeal
    is_card_yours = move.turn.user_id == card.user_table_id
    if fd:
        if is_card_yours:
            ForcedDeal.objects.filter(
                id=fd.id,
                offered=None
            ).update(offered=card)
        elif fd.requested and (card == fd.requested or card.is_say_no):
            ForcedDeal.objects.filter(
                id=fd.id,
                received=None
            ).update(received=card)
            Card.objects.filter(
                id=card.id, user_table_id=card.user_id).update(
                user_table_id=move.turn.user_id)
            end_move(move)
        else:
            ForcedDeal.objects.filter(
                id=fd.id,
                requested=None
            ).update(requested=card)
