from set import SetCard, SetGame
from math import floor

WIDTH = 1000
HEIGHT = 800

cw = 200
ch = 100
border = 100
gap = 200

game = SetGame()

def draw_table():
    for i, card in game.table.items():
        if card is None:
            continue
        row = gap * floor(i / 4) + border
        col = gap * (i % 4) + border
        card.sprite.pos = (col, row)
        card.sprite.draw()
        if i in game.selected:
            outline = Actor('outline')
            outline.pos = card.sprite.pos
            outline.draw()

def update():
    screen.clear()
    screen.fill((255, 255, 255))
    draw_table()
    text = 'Available sets: {}'.format(len(game.available_sets))
    screen.draw.text(text, (50, 600), fontsize=100, color='black')
    text = 'Player points: {}'.format(len(game.player))
    screen.draw.text(text, (50, 700), fontsize=100, color='black')

def on_mouse_down(pos):
    for table_index, card in game.table.items():
        if card.sprite.collidepoint(pos):
            if table_index not in game.selected:
                game.selected.append(table_index)
                print('Added:', game.selected)
                if len(game.selected) == 3:
                    try:
                        game.take(*game.selected)
                        game.selected = []
                    except ValueError:
                        print('Not a valid set')
            else:
                selected_index = game.selected.index(table_index)
                game.selected.pop(selected_index)
                print('Removed:', game.selected)