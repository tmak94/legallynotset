"""This Module contains all information regarding GameStates"""
from .shapes import text_object
from .game import Game
from .button import Button
from .card import Card
from pygame import transform, font
from pygame import quit as pg_quit
import sys


class GameState:

    """
    A GameState is whatever is currently being presented to the User. This includes both visual output and User input.

    State 0: Title
    The Title GameState is the default GameState when the application is launched.
    It has three Buttons: "Start Game," "About," and "Exit."
    - Start Game changes the GameState to 1, which starts the Game
    - About changes the GameState to 3, which displays the Rules
    - Exit will close the application

    State 1: Game
    The Game GameState is where the game is. Details can be found in the Game module.

    State 2: Game Over
    The Game Over GameState is automatically triggered at the game's completion.
    It has two Buttons: "Play Again?" and "Back to Title."
    - Play Again? changes the GameState back to 1 and resets the game
    - Back to Title changes the GameState to 0

    State 3: Rules
    The About/Rules GameState only has one Button.
    - Back returns to Title GameState

    """

    state = 0

    def __init__(self):
        self.game = Game()
        self.titleButtons = [Button("New Game", self.startGame), Button("How To Play", self.rules),
                             Button("Quit", self.quit)]
        self.ruleButton = Button("Back", self.rTT)
        self.gameOverButtons = [Button("New Game", self.startGame), Button("Main Menu", self.rTT)]
        self.stateListRender = [self.renderTitle, self.game.renderGame, self.gameOverStateRender,
                                self.rulesStateRender]
        self.stateListUpdate = [self.titleButtonChecker, self.game.eventListener, self.gameOverButtonChecker,
                                self.ruleButton.clicked]


    def renderTitle(self, display):
        """
        Renders the visuals for the Title GameState

        Args:
            display: Where the game is rendered (expected to be pygame.display)
        """
        display.fill((200, 200, 200))
        title = text_object("Legally Not Set!", font.Font('freesansbold.ttf', 50))

        display.blit(title, (280, 100))

        self.titleButtons[0].drawButton(display, (370, 200))
        self.titleButtons[1].drawButton(display, (370, 285))
        self.titleButtons[2].drawButton(display, (370, 370))

    def startGame(self):
        """
        Prepares Game to be played
        Then changes the GameState to Game
        """
        self.game.resetGame()
        GameState.state = 1

    def rTT(self):
        """
        Changes GameState to Title
        """
        GameState.state = 0

    def rules(self):

        GameState.state = 3

    def quit(self):
        pg_quit()
        sys.exit()
        quit()




    def gameStateRender(self, display):
        """
        Determines which GameState should be rendered
        Dependent on GameState.state

        Args:
            display: Where the game is rendered (expected to be pygame.display)
        """
        self.stateListRender[GameState.state](display)

    def titleButtonChecker(self):
        for button in self.titleButtons:
            button.clicked()

    def gameOverButtonChecker(self):
        """
        Checks if any button is clicked for the Game Over Buttons
        """
        for button in self.gameOverButtons:
            button.clicked()

    def gameStateUpdate(self):
        """
        Runs all necessary checks for each Event in event.get
        Dependent on GameState.state
        """
        self.stateListUpdate[GameState.state]()

    def gameOverStateRender(self, display):
        """
        Renders the visuals for the Game Over GameState
        Args:
            display: Where the game is rendered (expected to be pygame.display)
        """
        display.fill((0, 0, 0))
        display.fill((200, 200, 200), ((131, 82), (655, 411)))
        display.blit(font.Font('freesansbold.ttf', 100).render("Game Over!", True, (0, 0, 0)), (160, 140))
        self.gameOverButtons[0].drawButton(display, (245, 350))
        self.gameOverButtons[1].drawButton(display, (465, 350))

    def rulesStateRender(self, display):
        cardText = ["There are four identifiers a Card has:",
               "The Number of Shapes (1, 2, or 3)",
               "The Shape Type (Rectangle, Oval, or Diamond)",
               "The Shape's Color (Red, Green, or Purple)",
               "The Shape's Fill-type (Solid, Outline, or Striped)"]

        triadText = ["A Triad is when 3 cards all have either the SAME identifier or all have DIFFERENT identifiers.",
                     "Each of the 4 identifiers must be the same/different between the 3 cards"]

        goodTriad1 = [Card(1, 2, 3, 1).render, Card(1, 2, 3, 2).render, Card(1, 2, 3, 3).render]
        goodTriad2 = [Card(1, 2, 3, 1).render, Card(2, 3, 1, 2).render, Card(3, 1, 2, 3).render]

        badTriad = [Card(1, 2, 3, 1).render,  Card(2, 3, 1, 1).render, Card(3, 1, 2, 2).render]

        display.fill((200, 200, 200))
        display.blit(font.Font('freesansbold.ttf', 50).render("How to Play", True, (0, 0, 0)), (330, 40))
        for text in cardText:
            display.blit(font.Font('freesansbold.ttf', 15).render(text, True, (0, 0, 0)),
                         (150, 160 + (15 * cardText.index(text))))

        display.blit(Card(2, 1, 2, 3).render, (520, 120))
        for text in triadText:
            display.blit(font.Font('freesansbold.ttf', 13).render(text, True, (0, 0, 0)),
                         (210, 340 + (13 * triadText.index(text))))

        for card in goodTriad1:
            smallCard = transform.smoothscale(card, (75, 88))
            display.blit(smallCard, (30 + (80 * goodTriad1.index(card)), 370))
        display.blit(font.Font('freesansbold.ttf', 20).render("YES", True, (0, 0, 0)), (130, 470))

        for card in goodTriad2:
            smallCard = transform.smoothscale(card, (75, 88))
            display.blit(smallCard, (330 + (80 * goodTriad2.index(card)), 370))
        display.blit(font.Font('freesansbold.ttf', 20).render("YES", True, (0, 0, 0)), (430, 470))

        for card in badTriad:
            smallCard = transform.smoothscale(card, (75, 88))
            display.blit(smallCard, (630 + (80 * badTriad.index(card)), 370))
        display.blit(font.Font('freesansbold.ttf', 20).render("NO", True, (0, 0, 0)), (730, 470))

        self.ruleButton.drawButton(display, (350, 500))
