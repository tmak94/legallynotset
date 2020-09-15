
from modules.gStateHandler import *
from pygame import init, display, time, QUIT, MOUSEBUTTONDOWN, event
from pygame import quit as pg_quit


init()
display.set_caption("Legally Not Set!")
win = display.set_mode((915, 575))
clock = time.Clock()
newGame = GameState()


run = True
while run:
    newGame.gameStateRender(win)


    for ent in event.get():

        if ent.type == MOUSEBUTTONDOWN and ent.button == 1:
            newGame.gameStateUpdate()

        if ent.type == QUIT:
            run = False
            pg_quit()
            sys.exit()
            quit()


    display.update()


pg_quit()
sys.exit()
quit()
