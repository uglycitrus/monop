from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt

from .services import flip as flip_service
from .models import Card


@csrf_exempt
def flip(request, card_id):
    card = get_object_or_404(Card, pk=card_id)
    flip_service(card, request.user.id)
    return JsonResponse({'success': True, })
