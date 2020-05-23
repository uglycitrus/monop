from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt

from deck.models import Card
from .models import Payment
from .services import (
    assign_victim as assign_victim_service,
    pay as pay_service,
)


@csrf_exempt
def pay(request, payment_id, card_id):
    payment = get_object_or_404(Payment, pk=payment_id)
    card = get_object_or_404(Card, pk=card_id, user_table_id=request.user.id)
    pay_service(payment, card, request.user.id)
    return JsonResponse({'success': True, })


@csrf_exempt
def assign_victim(request, payment_id, victim_id):
    assign_victim_service(payment_id, victim_id, request.user.id)
    return JsonResponse({'success': True, })
