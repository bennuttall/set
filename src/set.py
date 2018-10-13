from itertools import product, combinations
from random import shuffle
from pgzero.actor import Actor

COLORS = ('red', 'green', 'purple')
SHAPES = ('diamond', 'squiggle', 'oval')
SHADINGS = ('solid', 'striped', 'open')
NUMBERS = (1, 2, 3)

class SetCard:
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
        self.sprite = Actor('{}{}{}{}'.format(color, shape, shading, number))

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
        self.table = {i: self.deck.pop() for i in range(12)}
        self.player = []
        self.selected = []
        self.available_sets = self.get_available_sets()

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
            for ci in cards:
                self.player.append(self.table.pop(ci))
                try:
                    self.table[ci] = self.deck.pop()
                except IndexError:
                    self.table[ci] = None
            self.available_sets = self.get_available_sets()
        else:
            raise ValueError('Not a valid set')

    def get_available_sets(self):
        all_cards = [card for card in self.table.values() if card is not None]
        possible_sets = combinations(all_cards, 3)
        valid_sets = [cards for cards in possible_sets if valid_set(*cards)]
        for cards in valid_sets:
            print('Valid set:', cards)
        return valid_sets