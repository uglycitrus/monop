from django.db import models
from django.db.models import Sum
from django.conf import settings

class PaymentManager(models.Manager):
    def unpaid(self):
        total = self.received.annotate(sum=Sum('dollar_value'))

class Payment(models.Model):
    move = models.ForeignKey(
        'turn.Move',
        on_delete=models.CASCADE,
        related_name='payments')
    amount = models.IntegerField()
    victim = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        null=True,
        blank=True)
    received = models.ManyToManyField('deck.Card')

    class Meta:
        db_table = 'payment'

    def is_paid(self):
        total = self.received.aggregate(sum=Sum('dollar_value'))
        return (total['sum'] or 0) >= self.amount
