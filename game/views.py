from django.http import HttpResponse, JsonResponse
from django.template import loader
from django.shortcuts import get_object_or_404, render
from django.views.decorators.csrf import csrf_exempt

from deck.constants import MONOPOLIES
from .models import Game
from .services import status, start_turn as start_turn_service

MONEYS = (1, 2, 3, 4, 5, 10, )


def list(request):
    return render(
        request,
        'game_list.html',
        context={'games': Game.objects.filter(users=request.user)})


def detail(request, game_id):
    game_status = status(get_object_or_404(Game, pk=game_id), request.user)
    return render(
        request,
        'index.html',
        context={
            'status': game_status,
            'monopolies': dict(MONOPOLIES),
            'moneys': MONEYS,
        }
    )


@csrf_exempt
def start_turn(request, game_id):
    start_turn_service(get_object_or_404(Game, pk=game_id))
    return JsonResponse({'success': True, })
