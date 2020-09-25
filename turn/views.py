import json

from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt

from deck.models import Card
from .services import move, end_turn, pick as pick_service
from .models import Turn


@csrf_exempt
def pick(request, turn_id, card_id):
    turn = get_object_or_404(Turn, pk=turn_id)
    card = get_object_or_404(Card, pk=card_id, game_id=turn.game_id)
    move = turn.get_active_move()
    if move:
        pick_service(move, card, request.user.id)
    return JsonResponse({'success': True, })


@csrf_exempt
def end(request, turn_id):
    # TODO: end_turn doesn't require a user_id. what happens if req unauthed
    turn = get_object_or_404(Turn, pk=turn_id)
    end_turn(turn, request.user.id)
    return JsonResponse({'success': True, })


@csrf_exempt
def play(request, turn_id, card_id):
    if json.loads(request.read() or '{}').get('discard'):
        discard(
            turn=Turn.objects.get(id=turn_id),
            card=Card.objects.get(id=card_id),
            user_id=request.user.id,
        )
    else:
        move(
            turn=Turn.objects.get(id=turn_id),
            card=Card.objects.get(id=card_id),
            user_id=request.user.id,
            as_cash=json.loads(request.read() or '{}').get('as_cash'))
    return JsonResponse({'success': True, })
