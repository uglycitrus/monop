from collections import defaultdict

from deck.services import build_deck, deal, DeckStatus, draw
from turn.services import end_turn, end_move
from .models import Game, Player


def new_game(*users):
    if not (1 <= len(users) <= 4):
        raise Exception('this is a game for 2-5 players')
    game = Game.objects.create()
    for index, user in enumerate(users):
        Player.objects.create(user=user, game=game, order=index)
    build_deck(game.id)
    deal(game.id, *[i.id for i in users])
    return game


def start_turn(game):
    user = Player.objects.get(
        game_id=game.id,
        order=(game.turns.count() % game.users.count())).user
    new_turn = game.turns.create(is_active=True, user=user)
    draw(game.id, user.id)
    return new_turn


def whos_turn(game):
    turn = game.get_active_turn()
    if turn:
        active_move = turn.get_active_move()
        if not active_move and turn.moves.count() >= 3:
            end_turn(turn, None)
            turn = start_turn(game)
        elif active_move and active_move.is_complete():
            turn = end_move(active_move)
    else:
        turn = start_turn(game)
    return turn


def make_winner(game, user_id):
    Player.objects.filter(
        game=game,
        user=user_id,
        is_winner=None).update(is_winner=True)

def _payment_action_mapper(turn, user, active_move):
    if turn.user == user:
        payment = active_move.payments.filter(victim__isnull=True).first()
        if payment:
            return {
                'type': 'Pick Payment Victim',
                'payment_id': payment.id,
            }
    return {
        'type': 'payment',
        'payments': {p.victim.id if p.victim else None: {
                'id': p.id,
                'amount': p.amount,
                'victim': p.victim.username if p.victim else None,
            }
            for p in active_move.payments.all()
        },
    }


def _action_picker(turn, user):
    active_move = turn.get_active_move()
    if active_move:
        if active_move.payments.exists():
            return _payment_action_mapper(turn, user, active_move)
        elif active_move.forceddeal:
            if not (active_move.forceddeal.offered_id and active_move.forceddeal.requested_id): 
                return {'type': 'ForcedDeal1', 'id': active_move.forceddeal.id}
            else:
                return {
                    'type': 'ForcedDeal2',
                    'id': active_move.forceddeal.id,
                    'highlighted_cards': [
                        active_move.forceddeal.offered_id,
                        active_move.forceddeal.requested_id,
                    ]
                }
            
        else:
            return {'type': 'action is happening'}
    else:
        if turn.user == user:
            return {'type': 'end_turn'}
        else:
            return {'type': 'wait'}


def status(game, user):
    deck_status = DeckStatus(game.id, user.id)
    deck_status.get_status()
    players = Player.objects.filter(game=game)
    rtrn = {
        'winner': deck_status.winner_id,
        'hand': deck_status.hand,
        'game_id': game.id,
        'users': {
            p.user_id: {
                'name': p.user.username,
                'cards': deck_status.visible_cards[p.user_id],
            } for p in players
        }
    }
    if deck_status.winner_id:
        make_winner(game, deck_status.winner_id)
        rtrn.update({
            'turn': None,
	    'action': None,
        })
    else:
        turn = whos_turn(game)
        rtrn.update({
	    'action': _action_picker(turn, user),
            'turn': {
                'id': turn.id,
                'user': turn.user_id,
                'move_number': turn.moves.count(),
            },
        })
    return rtrn
