import json
from collections import Counter

from .deck_rules import DECK_RULES


MONOPOLIES = Counter()
for i in DECK_RULES['property']:
    MONOPOLIES[i['color']] += 1

RENT_VALUES = {i['color']: i['rent_values'] for i in DECK_RULES['property']}
