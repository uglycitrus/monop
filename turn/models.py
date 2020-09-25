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
        null=True,
        on_delete=models.CASCADE,
        related_name='forced_deal_offered')
    requested = models.ForeignKey(
        'deck.Card',
        null=True,
        on_delete=models.CASCADE,
        related_name='forced_deal_requested')
    received = models.ForeignKey(
        'deck.Card',
        null=True,
        on_delete=models.CASCADE,
        related_name='forced_deal_received')

    class Meta:
        db_table = 'forced_deal'


class SlyDeal(models.Model):
    move = models.OneToOneField('Move', on_delete=models.CASCADE)
    requested = models.ForeignKey(
        'deck.Card',
        null=True,
        on_delete=models.CASCADE,
        related_name='sly_deal_requested')
    received = models.ForeignKey(
        'deck.Card',
        null=True,
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

    def is_complete(self):
        return (
            self.is_paid()
            and self.is_deal_breaker_done()
            and self.is_forced_deal_done()
            and self.is_sly_deal_done()
        )

    def get_deal_breaker(self):
        try:
            return self.dealbreaker
        except DealBreaker.DoesNotExist:
            return None

    def is_deal_breaker_done(self):
        db = self.get_deal_breaker()
        return db.received.exists() if db else True

    def get_sly_deal(self):
        try:
            return self.slydeal
        except SlyDeal.DoesNotExist:
            return None

    def is_sly_deal_done(self):
        sd = self.get_sly_deal()
        return sd.received if sd else True

    def get_forced_deal(self):
        try:
            return self.forceddeal
        except ForcedDeal.DoesNotExist:
            return None

    def is_forced_deal_done(self):
        fd = self.get_forced_deal()
        return fd.received if fd else True

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

    def user_needs_discard(self):
        return self.user.hand_cards.filter(game=self.game).count() > 7
