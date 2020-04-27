from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from .services import flip as flip_service


@csrf_exempt
def flip(request, card_id):
    flip_service(card_id, request.user.id)
    return JsonResponse({'success': True, })
