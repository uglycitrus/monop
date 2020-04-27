from collections import defaultdict

from django.core.exceptions import ObjectDoesNotExist

from deck.services import build_deck, deal, DeckStatus, draw
from turn.services import end_turn
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
    try:
        turn = game.turns.get(is_active=True)
    except ObjectDoesNotExist:
        turn = start_turn(game)
    else:
        if turn.moves.count() >= 3:
            end_turn(turn.id, None)
            turn = start_turn(game)
    return turn


def make_winner(game, user_id):
    Player.objects.filter(
        game=game,
        user=user_id,
        is_winner=None).update(is_winner=True)


def _action_picker(turn, user):
    try:
        active_move = turn.moves.get(is_active=True)
    except ObjectDoesNotExist:
        active_move = None
    if active_move:
        if active_move.payments.exists():
            return 'payment'
        else:
            return 'action is happening'
    else:
        if turn.user == user:
            return 'end_turn'
        else:
            return 'wait'


def status(game, user):
    deck_status = DeckStatus(game.id, user.id)
    deck_status.get_status()
    players = Player.objects.filter(game=game)
    rtrn = {
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
            'winner': deck_status.winner_id,
            'turn': None,
	    'action': None,
        })
    else:
        turn = whos_turn(game)
        rtrn.update({
            'winner': None,
	    'action': _action_picker(turn, user),
            'turn': {
                'id': turn.id,
                'user': turn.user_id,
                'move_number': turn.moves.count(),
            },
        })
    return rtrn
