from django.db import models
from django.conf import settings


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


class Payment(models.Model):
    move = models.ForeignKey('Move', on_delete=models.CASCADE, related_name='payments')
    amount = models.IntegerField()
    victim = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        null=True,
        blank=True)
    received = models.ManyToManyField('deck.Card')

    class Meta:
        db_table = 'payment'


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
