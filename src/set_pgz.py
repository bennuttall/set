from itertools import product
from random import shuffle
from math import floor

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
        self.table = [self.deck.pop() for i in range(12)]
        self.player = []
        self.selected = []

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
        else:
            raise ValueError('Not a valid set')

WIDTH = 1000
HEIGHT = 800

cw = 200
ch = 100
border = 100
gap = 200

game = SetGame()

def draw_table():
    for i, card in enumerate(game.table):
        row = gap * floor(i / 4) + border
        col = gap * (i % 4) + border
        card.sprite.pos = (col, row)
        card.sprite.draw()

def update():
    screen.clear()
    screen.fill((255, 255, 255))
    draw_table()

def on_mouse_down(pos):
    for card in game.table:
        if card.sprite.collidepoint(pos):
            table_index = game.table.index(card)
            if table_index not in game.selected:
                game.selected.append(table_index)
                print('Added', game.selected)
                if len(game.selected) == 3:
                    try:
                        game.take(*game.selected)
                        game.selected = []
                    except ValueError:
                        print('Not a valid set')
            else:
                selected_index = game.selected.index(table_index)
                game.selected.pop(selected_index)
                print('Removed', game.selected)
