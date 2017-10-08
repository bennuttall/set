from itertools import product
from random import shuffle

COLORS = ('red', 'green', 'purple')
SHAPES = ('diamond', 'squiggle', 'oval')
SHADINGS = ('solid', 'striped', 'open')
NUMBERS = (1, 2, 3)

class SetCard:
    """
    Represents a single Set game card. Create a card specifying a valid color,
    shape, shading and number:

    SetCard(color, shape, shading, number)

    color (str): red, green or purple
    shape (str): diamond, squiggle or oval
    shading (str): solid, striped or open
    number (int): 1, 2 or 3

    e.g:

    >>> card = SetCard(color='red', shape='diamond', shading='solid', number=1)
    """
    def __init__(self, color, shape, shading, number):
        if color not in COLORS:
            raise ValueError(
                'Invalid color: must be one of {}, {} or {}'.format(*COLORS)
            )
        if shape not in SHAPES:
            raise ValueError(
                'Invalid shape: must be one of {}, {} or {}'.format(*SHAPES)
            )
        if shading not in SHADINGS:
            raise ValueError(
                'Invalid shading: must be one of {}, {} or {}'.format(*SHADINGS)
            )
        if number not in NUMBERS:
            raise ValueError(
                'Invalid number: must be one of {}, {} or {}'.format(*NUMBERS)
            )
        self.color = color
        self.shape = shape
        self.shading = shading
        self.number = number

    def __repr__(self):
        return '<SetCard object: {} {} {} {}>'.format(
            self.color, self.shape, self.shading, self.number
        )

def _validate(properties):
    return len(properties) != 2

def valid_set(card_1, card_2, card_3):
    cards = (card_1, card_2, card_3)
    colors = {card.color for card in cards}
    shapes = {card.shape for card in cards}
    shadings = {card.shading for card in cards}
    numbers = {card.number for card in cards}
    properties = (colors, shapes, shadings, numbers)
    return all(_validate(p) for p in properties)

class SetGame:
    def __init__(self, random=True):
        self.deck = self._create_deck(random)
        self.table = [self.deck.pop() for i in range(12)]
        self.player = []

    def _create_deck(self, random):
        combinations = product(COLORS, SHAPES, SHADINGS, NUMBERS)
        deck = [SetCard(*c) for c in combinations]
        if random:
            shuffle(deck)
        return deck

    def take(self, card_1_index, card_2_index, card_3_index):
        card_1 = self.table[card_1_index]
        card_2 = self.table[card_2_index]
        card_3 = self.table[card_3_index]
        if valid_set(card_1, card_2, card_3):
            cards = (card_1_index, card_2_index, card_3_index)
            self.player.extend(self.table.pop(ci) for ci in cards)
            self.table.extend(self.deck.pop(i) for i in range(3))
