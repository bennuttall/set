from set import *
import pytest

# test creating valid cards
card = SetCard(color='red', shape='diamond', shading='solid', number=1)
card = SetCard(color='green', shape='squiggle', shading='striped', number=2)
card = SetCard(color='purple', shape='oval', shading='open', number=3)

# test creating invalid cards
with pytest.raises(TypeError):
    SetCard()
with pytest.raises(TypeError):
    SetCard(color='red')
with pytest.raises(TypeError):
    SetCard(color='red', shape='diamond', shading='solid')
with pytest.raises(ValueError):
    SetCard(color='red', shape='diamond', shading='solid', number=4)
with pytest.raises(ValueError):
    SetCard(color='pink', shape='diamond', shading='solid', number=4)
with pytest.raises(ValueError):
    SetCard(color='diamond', shape=1, shading='shading', number=1)

# test card attributes
card = SetCard(color='red', shape='diamond', shading='solid', number=1)
assert card.color == 'red'
assert card.shape == 'diamond'
assert card.shading == 'solid'
assert card.number == 1

# test validating invalid sets
with pytest.raises(TypeError):
    valid_set()

card_1 = SetCard(color='red', shape='diamond', shading='solid', number=1)
with pytest.raises(TypeError):
    valid_set(card_1)

card_2 = SetCard(color='red', shape='diamond', shading='solid', number=2)
with pytest.raises(TypeError):
    valid_set(card_1, card_2)

card_3 = SetCard(color='red', shape='diamond', shading='open', number=1)
assert not valid_set(card_1, card_2, card_3)

# test validating valid sets
card_4 = SetCard(color='red', shape='diamond', shading='solid', number=3)
assert valid_set(card_1, card_2, card_4)

card_1 = SetCard(color='red', shape='diamond', shading='solid', number=1)
card_2 = SetCard(color='green', shape='squiggle', shading='striped', number=2)
card_3 = SetCard(color='purple', shape='oval', shading='open', number=3)
assert valid_set(card_1, card_2, card_3)

deck_size = 3**4
table_size = 12
set_size = 3

def table_len(table):
    return len([v for v in table.values() if v])

# test creating set game
game = SetGame(random=False)
assert table_len(game.table) == table_size
assert len(game.deck) == deck_size - table_size
assert len(game.player) == 0

# test taking invalid set in a game
with pytest.raises(ValueError):
    game.take(0, 1, 3)
assert table_len(game.table) == table_size
assert len(game.deck) == deck_size - table_size
assert len(game.player) == 0

with pytest.raises(ValueError):
    game.take(0, 1, 4)
assert table_len(game.table) == table_size
assert len(game.deck) == deck_size - table_size
assert len(game.player) == 0

# test taking valid sets in a game
game.take(0, 1, 2)
assert table_len(game.table) == table_size
assert len(game.deck) == deck_size - table_size - set_size
assert len(game.player) == set_size

game.take(6, 7, 8)
assert table_len(game.table) == table_size
assert len(game.deck) == deck_size - table_size - 2 * set_size
assert len(game.player) == 2 * set_size

print("Tests passing!")