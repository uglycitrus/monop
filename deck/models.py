import random

from django.db import models
from django.conf import settings

from .constants import RENT_VALUES
from .deck_rules import (
    DECK_RULES, SLY_DEAL, FORCED_DEAL, DEAL_BREAKER, PASS_GO, DEBT_COLLECTOR,
    BIRTHDAY, RENT, DOUBLE_RENT, PROPERTY, PROPERTY_WILD, SAY_NO,
)


COLOR_CHOICES = tuple((color, color) for color in RENT_VALUES.keys())
CARD_CHOICES = tuple((k, k) for k in DECK_RULES.keys())


class DrawPileManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_drawn=False)

    def draw(self, game_id, user_id, count=2):
        ids = set(self.get_queryset().filter(
            game_id=game_id).values_list('id', flat=True))
        # TODO: if ids < count, shuffle
        draw_ids = random.sample(ids, count)
        self.get_queryset().filter(id__in=draw_ids).update(
            is_drawn=True,
            user_hand_id=user_id)
        return draw_ids 


class Card(models.Model):
    game = models.ForeignKey(
        'game.Game',
        on_delete=models.CASCADE,
        related_name='cards')
    is_drawn = models.BooleanField(default=False)
    card_type = models.CharField(max_length=255, choices=CARD_CHOICES)
    color = models.CharField(max_length=255, choices=COLOR_CHOICES)
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    secondary_color = models.CharField(max_length=255, choices=COLOR_CHOICES)
    dollar_value = models.IntegerField(null=True)
    victim_limit = models.IntegerField(null=True)
    victim_amount = models.IntegerField(null=True)
    user_hand = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='hand_cards')
    user_table = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='table_cards')

    objects = models.Manager()
    draw_pile_objects = DrawPileManager()

    class Meta:
        db_table = 'card'

    @property
    def is_pass_go(self):
        return self.name == PASS_GO

    @property
    def is_property(self):
        return self.card_type in (PROPERTY, PROPERTY_WILD)

    @property
    def is_for_placing(self):
        """
        is this a card that is meant to be placed on your table?
        """
        return not self.is_for_playing

    @property
    def is_for_playing(self):
        """
        is this a card that is meant to be played into the discard pile?
        """
        return self.is_move_active or self.is_pass_go

    @property
    def is_move_active(self):
        return (
            self.is_sly_deal
            or self.is_forced_deal
            or self.is_deal_breaker
            or self.is_payment_generating
        )

    @property
    def is_sly_deal(self):
        return self.name == SLY_DEAL

    @property
    def is_forced_deal(self):
        return self.name == FORCED_DEAL

    @property
    def is_say_no(self):
        return self.name == SAY_NO

    @property
    def is_deal_breaker(self):
        return self.name == DEAL_BREAKER

    @property
    def is_rent(self):
        return self.card_type == RENT

    @property
    def is_payment_generating(self):
        return self.is_rent or self.name in (DEBT_COLLECTOR, BIRTHDAY)

    @property
    def is_double_rent(self):
        return self.name == DOUBLE_RENT
