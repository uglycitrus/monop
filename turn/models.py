from django.db import models
from django.db.models.functions import Coalesce
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist


class DealBreaker(models.Model):
    move = models.OneToOneField('Move', on_delete=models.CASCADE)
    requested = models.ManyToManyField(
        'deck.Card',
        related_name='deal_breaker_requested')
    received = models.ManyToManyField(
        'deck.Card',
        related_name='deal_breaker_received')

    class Meta:
        db_table = 'deal_breaker'


class ForcedDeal(models.Model):
    move = models.OneToOneField('Move', on_delete=models.CASCADE)
    offered = models.ForeignKey(
        'deck.Card',
        on_delete=models.CASCADE,
        related_name='forced_deal_offered')
    requested = models.ForeignKey(
        'deck.Card',
        on_delete=models.CASCADE,
        related_name='forced_deal_requested')

    class Meta:
        db_table = 'forced_deal'


class SlyDeal(models.Model):
    move = models.OneToOneField('Move', on_delete=models.CASCADE)
    requested = models.ForeignKey(
        'deck.Card',
        on_delete=models.CASCADE,
        related_name='sly_deal_requested')
    received = models.ForeignKey(
        'deck.Card',
        on_delete=models.CASCADE,
        related_name='sly_deal_received')

    class Meta:
        db_table = 'sly_deal'


class Move(models.Model):
    index = models.IntegerField()
    is_active = models.NullBooleanField(default=None)
    turn = models.ForeignKey(
        'Turn',
        on_delete=models.CASCADE,
        related_name='moves')
    card = models.ForeignKey('deck.Card', on_delete=models.CASCADE)

    class Meta:
        db_table = 'move'
        unique_together = (
            ('turn', 'index'),
            ('turn', 'is_active'),
        )

    def is_paid(self):
        return not (
            self.payments
                .annotate(paid=Coalesce(models.Sum('received__dollar_value'), 0))
                .filter(paid__lt=models.F('amount'))
                .exists()
        )


class Turn(models.Model):
    is_active = models.NullBooleanField(default=None)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    game = models.ForeignKey(
        'game.Game',
        on_delete=models.CASCADE,
        related_name='turns')

    class Meta:
        db_table = 'turn'
        unique_together = (
            ('game', 'is_active'),
        )

    def get_active_move(self):
        try:
            return self.moves.get(is_active=True)
        except ObjectDoesNotExist:
            return None
