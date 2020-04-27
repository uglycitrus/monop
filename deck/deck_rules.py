from collections import OrderedDict


SLY_DEAL = 'Sly Deal'
FORCED_DEAL = 'Forced Deal'
DEAL_BREAKER = 'Deal Breaker'
PASS_GO = 'Pass Go'
DEBT_COLLECTOR = 'Debt Collector'
BIRTHDAY = 'It\'s My Birthday'
RENT = 'rent'
DOUBLE_RENT = 'Double the Rent'
PROPERTY = 'property'
PROPERTY_WILD = 'property wild card'

BLACK = 'black'
BLUE = 'blue'
BROWN = 'brown'
GREEN = 'green'
LIGHT_GREEN = 'lightgreen'
LIGHT_BLUE = 'lightblue'
ORANGE = 'orange'
PINK = 'pink'
RED = 'red'
YELLOW = 'yellow'


DECK_RULES = {
    'action': [
        {
            'name': DEAL_BREAKER,
            'description': '',
            'dollar_value': 5,
            'count': 2,
        },
        {
            'name': 'Just Say No',
            'description': '',
            'dollar_value': 4,
            'count': 3,
        },
        {
            'name': SLY_DEAL,
            'description': '',
            'dollar_value': 3,
            'count': 3,
        },
        {
            'name': FORCED_DEAL,
            'description': '',
            'dollar_value': 3,
            'count': 4,
        },
        {
            'name': DEBT_COLLECTOR,
            'description': '',
            'dollar_value': 3,
            'count': 3,
            'victim_limit': 1,
            'victim_amount': 5,
        },
        {
            'name': BIRTHDAY,
            'description': '',
            'dollar_value': 2,
            'count': 3,
            'victim_amount': 2,
        },
        {
            'name': PASS_GO,
            'description': '',
            'dollar_value': 1,
            'count': 10,
        },
        {
            'name': 'House',
            'description': '',
            'dollar_value': 3,
            'count': 3,
        },
        {
            'name': 'Hotel',
            'description': '',
            'dollar_value': 4,
            'count': 3,
        },
        {
            'name': DOUBLE_RENT,
            'description': '',
            'dollar_value': 3,
            'count': 2,
        }
    ],

    PROPERTY: [
        {
            'name': 'Baltic Ave',
            'rent_values': [1, 2 ],
            'color': BROWN,
            'dollar_value': 1,
        },
        {
            'name': 'Mediterranean Ave',
            'rent_values': [1, 2 ],
            'color': BROWN,
            'dollar_value': 1,
        },
        {
            'name': 'Boardwalk',
            'rent_values': [3, 8 ],
            'color': BLUE,
            'dollar_value': 4,
        },
        {
            'name': 'Park Place',
            'rent_values': [3, 8 ],
            'color': BLUE,
            'dollar_value': 4,
        },
        {
            'name': 'Water Works',
            'rent_values': [1, 2 ],
            'color': LIGHT_GREEN,
            'dollar_value': 2,
        },
        {
            'name': 'Electric Company',
            'rent_values': [1, 2 ],
            'color': LIGHT_GREEN,
            'dollar_value': 2,
        },
        {
            'name': 'Connecticut Ave',
            'rent_values': [1, 2, 3 ],
            'color': LIGHT_BLUE,
            'dollar_value': 1,
        },
        {
            'name': 'Oriental Ave',
            'rent_values': [1, 2, 3 ],
            'color': LIGHT_BLUE,
            'dollar_value': 1,
        },
        {
            'name': 'Vermont Ave',
            'rent_values': [1, 2, 3 ],
            'color': LIGHT_BLUE,
            'dollar_value': 1,
        },
        {
            'name': 'New York Ave',
            'rent_values': [1, 3, 5 ],
            'color': ORANGE,
            'dollar_value': 2,
        },
        {
            'name': 'St James Place',
            'rent_values': [1, 3, 5 ],
            'color': ORANGE,
            'dollar_value': 2,
        },
        {
            'name': 'Tennessee Ave',
            'rent_values': [1, 3, 5 ],
            'color': ORANGE,
            'dollar_value': 2,
        },
        {
            'name': 'St Charles Place',
            'rent_values': [1, 2, 4 ],
            'color': PINK,
            'dollar_value': 2,
        },
        {
            'name': 'Virginia Ave',
            'rent_values': [1, 2, 4 ],
            'color': PINK,
            'dollar_value': 2,
        },
        {
            'name': 'States Ave',
            'rent_values': [1, 2, 4 ],
            'color': PINK,
            'dollar_value': 2,
        },
        {
            'name': 'Short Line',
            'rent_values': [1, 2, 3, 4 ],
            'color': BLACK,
            'dollar_value': 2,
        },
        {
            'name': 'B. & O. Railroad',
            'rent_values': [1, 2, 3, 4 ],
            'color': BLACK,
            'dollar_value': 2,
        },
        {
            'name': 'Reading Railroad',
            'rent_values': [1, 2, 3, 4 ],
            'color': BLACK,
            'dollar_value': 2,
        },
        {
            'name': 'Pennsylvania Railroad',
            'rent_values': [1, 2, 3, 4 ],
            'color': BLACK,
            'dollar_value': 2,
        },
        {
            'name': 'Kentucky Ave',
            'rent_values': [2, 3, 6 ],
            'color': RED,
            'dollar_value': 3,
        },
        {
            'name': 'Indiana Ave',
            'rent_values': [2, 3, 6 ],
            'color': RED,
            'dollar_value': 3,
        },
        {
            'name': 'Illinois Ave',
            'rent_values': [2, 3, 6 ],
            'color': RED,
            'dollar_value': 3,
        },
        {
            'name': 'Ventnor Ave',
            'rent_values': [2, 4, 6 ],
            'color': YELLOW,
            'dollar_value': 3,
        },
        {
            'name': 'Marvin Gardens',
            'rent_values': [2, 4, 6 ],
            'color': YELLOW,
            'dollar_value': 3,
        },
        {
            'name': 'Atlantic Ave',
            'rent_values': [2, 4, 6 ],
            'color': YELLOW,
            'dollar_value': 3,
        },
        {
            'name': 'North Carolina Ave',
            'rent_values': [2, 4, 7 ],
            'color': GREEN,
            'dollar_value': 4,
        },
        {
            'name': 'Pacific Ave',
            'rent_values': [2, 4, 7 ],
            'color': GREEN,
            'dollar_value': 4,
        },
        {
            'name': 'Pennsylvania Ave',
            'rent_values': [2, 4, 7 ],
            'color': GREEN,
            'dollar_value': 4,
        },
    ],

    PROPERTY_WILD: [
        {
            'color': BLUE,
            'secondary_color': GREEN,
            'dollar_value': 4,
        },
        {
            'color': LIGHT_BLUE,
            'secondary_color': BROWN,
            'dollar_value': 1,
        },
        {
            'count': 2,
            'description': 'this can be used as part of any set',
            'dollar_value': 0,
        },
        {
            'count': 2,
            'color': ORANGE,
            'secondary_color': PINK,
            'dollar_value': 2,
        },
        {
            'count': 2,
            'color': YELLOW,
            'secondary_color': RED,
            'dollar_value': 3,
        },
        {
            'color': GREEN,
            'secondary_color': BLACK,
            'dollar_value': 4,
        },
        {
            'color': LIGHT_BLUE,
            'secondary_color': BLACK,
            'dollar_value': 4,
        },
        {
            'color': LIGHT_GREEN,
            'secondary_color': BLACK,
            'dollar_value': 2,
        },
    ],

    RENT: [
        {
            'count': 3,
            'description': 'charge 1 player rent for any property',
            'victim_limit': 1,
        },
        {
            'color': BLUE,
            'secondary_color': GREEN,
            'dollar_value': 1,
        },
        {
            'color': BROWN,
            'secondary_color': LIGHT_BLUE,
            'dollar_value': 1,
        },
        {
            'color': PINK,
            'secondary_color': ORANGE,
            'dollar_value': 1,
        },
        {
            'color': BLACK,
            'secondary_color': LIGHT_GREEN,
            'dollar_value': 1,
        },
        {
            'color': RED,
            'secondary_color': YELLOW,
            'dollar_value': 1,
        },
    ],

    'money': [
        {
            'count': 1,
            'dollar_value': 10,
        },
        {
            'count': 6,
            'dollar_value': 1,
        },
        {
            'count': 5,
            'dollar_value': 2,
        },
        {
            'count': 3,
            'dollar_value': 3,
        },
        {
            'count': 3,
            'dollar_value': 4,
        },
        {
            'count': 2,
            'dollar_value': 5,
        },
    ]
}
