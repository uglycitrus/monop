from django.conf import settings
from django.db import models


class Player(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    game = models.ForeignKey('Game', on_delete=models.CASCADE)
    order = models.IntegerField()
    is_winner = models.NullBooleanField(default=None)

    class Meta:
        db_table = 'player'
        unique_together = (
            ('game', 'is_winner'),
            ('game', 'user'),
            ('game', 'order'),
        )


class Game(models.Model):
    users = models.ManyToManyField(settings.AUTH_USER_MODEL, through=Player)

    class Meta:
        db_table = 'game'
