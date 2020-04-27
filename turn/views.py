import json

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from deck.models import Card
from .services import move, end_turn
from .models import Turn


@csrf_exempt
def end(request, turn_id):
    # TODO: end_turn doesn't require a user_id. what happens if req unauthed
    end_turn(turn_id, request.user.id)
    return JsonResponse({'success': True, })


@csrf_exempt
def play(request, turn_id, card_id):
    as_cash = json.loads(request.read()).get('as_cash')
    move(
        turn=Turn.objects.get(id=turn_id),
        card=Card.objects.get(id=card_id),
        user_id=request.user.id,
        as_cash=as_cash)
    return JsonResponse({'success': True, })
