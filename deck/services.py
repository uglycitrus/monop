import uuid
from collections import defaultdict, Counter

from django.db.models import Count, F

from .models import Card
from .deck_rules import DECK_RULES, PROPERTY, PROPERTY_WILD
from .constants import RENT_VALUES, MONOPOLIES


DISPLAY_CARD_VALUES = (
    'id',
    'user_table_id',
    'name',
    'description',
    'card_type',
    'color',
    'secondary_color',
    'dollar_value',
)


def _rent_values_description(color):
    return '; '.join([f'${i}M' for i in RENT_VALUES[color]])


def _generate_description(card_type, **kwargs):
    description = kwargs.pop('description', '')
    if description:
        return description

    if card_type == 'property':
        return _rent_values_description(kwargs.pop('color'))
    elif card_type == 'property wild card':
        color = kwargs.get('color')
        rent_values1 = _rent_values_description(color)
        secondary_color = kwargs.get('secondary_color')
        rent_values2 = _rent_values_description(secondary_color)
        return f'{color}: {rent_values1}\n{secondary_color}: {rent_values2}'
    else:
        return ''


def build_deck(game_id):
    for card_type, kwarg_list in DECK_RULES.items():
        for kwargs in kwarg_list:
            kwargs = kwargs.copy()
            count = kwargs.pop('count', 1)
            description = _generate_description(card_type, **kwargs)
            kwargs.pop('description', None) # clear out description
            kwargs.pop('rent_values', None) # clear out description
            for i in range(count):
                Card.objects.create(
                    game_id=game_id,
                    card_type=card_type,
                    description=description,
                    **kwargs)


def deal(game_id, *user_ids):
    for user_id in user_ids:
        Card.draw_pile_objects.draw(game_id, user_id, 5)


def draw(game_id, user_id, pass_go=False):
    if pass_go:
        Card.draw_pile_objects.draw(game_id, user_id, 2)
    else:
        cnt = Card.objects.filter(game_id=game_id, user_hand_id=user_id).count()
        if cnt == 0:
            Card.draw_pile_objects.draw(game_id, user_id, 5)
        else:
            Card.draw_pile_objects.draw(game_id, user_id, 2)

def play(card_id, user_id):
    """
    Play a card from your hand into the played pile
    """
    Card.objects.filter(
        id=card_id, user_hand_id=user_id, user_table=None).update(
        user_hand=None, user_table=None)


def place(card_id, user_id):
    """
    Place a card from your hand on your table
    """
    Card.objects.filter(
        id=card_id, user_hand_id=user_id, user_table=None).update(
        user_hand=None, user_table=F('user_hand'))


def flip(card_id, user_id):
    """
    Place a card from your hand on your table
    """
    Card.objects.filter(
        id=card_id, user_hand_id=user_id, user_table=None).update(
        color=F('secondary_color'), secondary_color=F('color'))


def max_rent(user_id, rent_card=None):
    """
    Place a card from your hand on your table
    """
    kwargs = {
        'user_hand_id': None,
        'user_table_id': user_id,
        'card_type__in': (PROPERTY, PROPERTY_WILD),
    }
    if rent_card and rent_card.color:
        kwargs['color__in'] =(rent_card.color, rent_card.secondary_color)
    sets = Card.objects.filter(**kwargs).values(
        'color').annotate(cnt=Count('color'))
    max_rent_amount = 0
    for s in sets:
        color = s['color']
        rent_scale = RENT_VALUES.get(color, [])
        cnt = min(s['cnt'], len(rent_scale)) - 1
        if cnt > 0:
            amount = rent_scale[cnt]
        else:
            continue
        if amount > max_rent_amount:
            max_rent_amount = amount 
    return max_rent_amount
        

class DeckStatus():
    def __init__(self, game_id, user_id):
        self.game_id = game_id
        self.user_id = user_id
        self.winner_id = None
        self.hand = []
        self.cards = Card.objects.filter(game_id=game_id)
        self.visible_cards = defaultdict(lambda: {
            'table': {
                'money': defaultdict(lambda: []),
                'property': defaultdict(lambda: []),
            },
            'hand_count': 0,
            'monopolies': [],
        })

    def get_status(self):
        self._hand_cards()
        self._table_cards()
        self._get_winner()
        return self.visible_cards

    def _get_winner(self):
        monopoly_status = Counter()
        for user_id, cards in self.visible_cards.items():
            for color, count in monopoly_status.items():
                count = len(cards.get('table').get('property').get(color))
                if MONOPOLIES[color] <= count:
                   self.visible_cards[user_id]['monopolies'].append(color)
            if len(self.visible_cards[user_id]['monopolies']) > 3:
                self.winner_id = user_id

    def _hand_cards(self):
        cards = self.cards.exclude(user_hand_id=None)
        for i in cards.values('user_hand').annotate(cnt=Count('user_hand')):
            if i['user_hand']:
                self.visible_cards[i['user_hand']]['hand_count'] = i['cnt']
        self.hand = self.cards.filter(
            user_hand_id=self.user_id).values(
            *DISPLAY_CARD_VALUES)

    def _table_cards(self):
        table_cards = self.cards.exclude(user_table=None)
        for card in table_cards:
            card_dict = {k: getattr(card, k) for k in DISPLAY_CARD_VALUES}
            table = self.visible_cards[card_dict.pop('user_table_id')]['table']
            if card.is_property:
                table['property'][card.color].append(card_dict)
            else:
                table['money'][card.dollar_value].append(card_dict)
