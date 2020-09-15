"""This Module defines the Game Class and its functions"""

import random
from itertools import combinations
from .card import Card
from .shapes import sideMenu
from .button import Button



class Game:
    """
    Legally Not Set is a game about finding consistent similarities and differences between Cards.

    There are 81 Cards, one for every permutation of Number, Shape, Color, and Fill-type identifiers. At the start
    of the game, 12 Cards are revealed, and the User must find 3 cards that make a Triad. A Triad is when
    3 cards all have either the SAME identifier (such as all 3 cards being Red or Stripped) or all have DIFFERENT
    identifiers (such as all 3 having different Numbers of Shapes or being different Shapes). Each of the 4 identifiers
    must be the same/different between the 3 cards (e.g. if two Cards have Circles and one has a Rectangle, it is NOT
    a Triad, even if all their other identifiers are the same/different). Once a Triad is made, those 3 Cards are
    removed from play and replaced with 3 new Cards. This continues until there are no possible Triads that can be made
    with the remaining Cards.

    The magic of Legally Not Set is that there will always be a Triad for the Player to find! This game tracks every
    combination of 2 Card IDs currently in play to calculates the third 'Solution' ID needed to make them a Triad.
    When a Triad is made, before the cards are replaced, the game checks if the IDs any of the currently remaining Cards
    are a 'Solution' ID. If not, the game searches the deck to find a Card with a 'Solution' ID. If it finds one, that
    Card is taken from the deck and put into play along with 2 additional Cards that are randomly selected. This ensures
    that there will always be at least one Triad for the Player to find!


        Attributes:
            newDeck: A List of 81 Cards that's generated and shuffled
            cardsInPlay: A List that holds the 12 Cards currently face up
            claimedCards: A List that holds Cards after User claims them
            idListInPlay: A List that holds the IDs of these 12 cards
            solutionIds: A Dictionary with ID combination Keys and their Solution value
            selectedCards: A List that holds the Cards the User has selected
            score: The integer count of the claimed Sets
            buttons: A List of Buttons used to navigate the Application

    """

    def __init__(self):
        self.cardPos = [(10, 15), (175, 15), (340, 15), (505, 15),
               (10, 200), (175, 200), (340, 200), (505, 200),
               (10, 385), (175, 385), (340, 385), (505, 385)]
        newDeck = []
        for a in range(1, 4):
            for b in range(1, 4):
                for c in range(1, 4):
                    for d in range(1, 4):
                        newDeck.append(Card(a, b, c, d))
        random.shuffle(newDeck)
        self.newDeck = newDeck
        self.cardsInPlay = []
        self.claimedCards = []
        self.idListInPlay = []
        self.solutionIds = {}
        self.selectedCards = []
        self.score = 0
        self.buttons = [Button("Shuffle", self.shuffleCards), Button("Reset Game", self.resetGame),
                        Button("Back to Title", self.rTT)]


    def startGame(self):
        """
        Starts the game by removing 12 Cards from the deck and track their IDs
        Then, take every combination of 2 IDs and find their Solution ID
        If there are no valid Combos, reset
        """
        for x in range(12):
            card = self.newDeck.pop()
            self.cardsInPlay.append(card)
            self.idListInPlay.append(card.getID())

        idComboStart = combinations(self.idListInPlay, 2)
        for combos in idComboStart:
            self.solutionIds[frozenset(combos)] = self.getSolutionId(combos[0], combos[1])

        if self.checkBoard():
            print("yay!")
        else:
            print("uh oh!")
            self.resetGame()


    def getSolutionId(self, id1, id2):
        """
        Generates the ID of the Card needed to make a Combo with the 2 Input Cards.

        Args:
            id1: The ID of Card 1
            id2: The ID of Card 2

        Returns: The ID of Card 3

        """
        solId = 0
        for i in range(4):
            d1 = id1 // 10**i % 10
            d2 = id2 // 10**i % 10
            if d1 == d2:
                d3 = d1
            else:
                d3 = 6 - d1 - d2
            solId += d3 * 10**i
        return solId

    def renderGame(self, display):
        """
        Creates the visual representation of the Game.
        The rendered parts of the Game are the Cards in Play and the Buttons.
        The Score and Remaining Cards are rendered as an integer count.

        Args:
            display: Where the game is rendered (expected to be pygame.display)
        """
        display.fill((0, 0, 0))


        display.blit(sideMenu(self.score, len(self.newDeck)), (665, 0))


        self.buttons[0].drawButton(display, (690, 300))
        self.buttons[1].drawButton(display, (690, 380))
        self.buttons[2].drawButton(display, (690, 460))


        for card in self.cardsInPlay:

            card.renderCard(display, self.cardPos[self.cardsInPlay.index(card)], self.selectedCards)





    def eventListener(self):
        """
        Checks if any Card or Button is pressed after the User clicks the LMB,
        also checks if the User has selected 3 Cards
        """
        for card in self.cardsInPlay:
            card.highlight(self.selectedCards)
        for button in self.buttons:
            button.clicked()
        if len(self.selectedCards) == 3:
            self.checkSet()

    def shuffleCards(self):
        """
        Rearranges the Cards in Play.
        Meant to help Users find Triads by looking at a different perspective
        """
        random.shuffle(self.cardsInPlay)

    def checkSet(self):
        """
        When 3 Cards are selected, the first 2 Cards are made into a frozenset that's used to reference the
        SolutionIDs dictionary. If the Value of the frozenset Key is the third selected card, then they are a Triad.
        If they are a Triad, those Cards are removed and new Cards are drawn.

        Otherwise, they are not a Triad.
        The selected Cards are cleared either way.
        """
        c12 = frozenset([self.selectedCards[0], self.selectedCards[1]])
        c3 = self.selectedCards[2]
        if self.solutionIds[c12] == c3:
            self.score += 1
            print("yes!")
            self.newCards()
        else:
            print("no!")
        self.selectedCards.clear()

    def newCards(self):
        """
        Removes the Selected Cards in play and any references to them in other Lists.
        Then, checks if there are any Combos with the remaining Cards in play
        Then, replaces the removed cards appropriately.

        Returns: Nothing (in the event no Cards are left)

        """
        for i in self.selectedCards:
            self.claimedCards.append(self.cardsInPlay[self.cardsInPlay.index(i)])
        self.solutionIds = {k:v for (k,v) in self.solutionIds.items() if len(k & set(self.selectedCards)) == 0}
        self.idListInPlay = [id for id in self.idListInPlay if id not in self.selectedCards]
        self.cardsInPlay = [card for card in self.cardsInPlay if card.getID() not in self.selectedCards]
        tempCardList = []
        if not self.checkBoard() and (not self.anySolCardLeft()):
            self.gameOver()
            return
        elif self.checkBoard() and len(self.newDeck) > 0:
            print("you good")
            tempCardList = self.anyCard()
        elif not self.checkBoard() and self.anySolCardLeft():
            print("i got u fam")
            tempCardList = self.guarenteedCard()
        for card in tempCardList:
            self.cardsInPlay.append(card)
            for i in self.idListInPlay:
                self.solutionIds[frozenset([i, card.id])] = self.getSolutionId(i,card.id)
            self.idListInPlay.append(card.id)

    def resetGame(self):
        """
        Resets the game
        First, resets the score to 0
        Then, clears the list of selected Cards
        Then, moves all Claimed Cards back to the deck
        Then, moves all remaining Cards in Play back to the deck
        Then, clears the cross-reference databases
        Then, Shuffles the Deck
        Finally, Starts Game
        """
        self.score = 0
        self.selectedCards.clear()
        self.newDeck.extend(self.claimedCards)
        self.claimedCards.clear()
        self.newDeck.extend(self.cardsInPlay)
        self.cardsInPlay.clear()
        self.idListInPlay.clear()
        self.solutionIds.clear()
        random.shuffle(self.newDeck)
        self.startGame()



    def checkBoard(self):
        """
        Checks if any IDs of the Cards in play are also a Solution ID

        Returns: Boolean

        """
        return any(id in self.idListInPlay for id in list(self.solutionIds.values()))

    def guarenteedCard(self):
        """
        Finds the first Card in the Deck with a Solution ID,
        Then puts it in a List with the next 2 Cards in the Deck
        Then shuffles those 3 Cards


        Returns: A List of 3 Cards

        """
        tempCardList = []
        for i in range(len(self.newDeck)):
            if self.newDeck[i].id in self.solutionIds.values():
                tempCardList.append(self.newDeck.pop(i))
                break
        tempCardList.append(self.newDeck.pop())
        tempCardList.append(self.newDeck.pop())
        random.shuffle(tempCardList)
        return tempCardList

    def anyCard(self):
        """
        Pops the first 3 Cards off of the Deck

        Returns: A List of 3 Cards

        """
        tempCardList = []
        for i in range(3):
            tempCardList.append(self.newDeck.pop())
        return tempCardList


    @staticmethod
    def rTT():
        """
        Returns to Title.
        """
        from .gStateHandler import GameState
        GameState.state = 0

    @staticmethod
    def gameOver():
        """
        Brings up the Game Over screen.
        Used when there are no possible Triads left for the Player to make
        """
        from .gStateHandler import GameState
        GameState.state = 2

    def anySolCardLeft(self):
        return any(ids in self.newDeck for ids in self.solutionIds.values())
